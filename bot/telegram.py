import asyncio
from decimal import Decimal

from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import CallbackQuery, Message
from asgiref.sync import sync_to_async
from django.conf import settings

from shop.models import Category, Product, TelegramUser
from shop.services import add_to_cart, clear_cart, create_order_from_cart, get_or_create_user

from .keyboards import (
    add_to_cart_keyboard,
    cart_actions_keyboard,
    language_keyboard,
    menu_keyboard,
)
from .messages import t

router = Router()

# Singletons to avoid re-attaching router
_bot_instance = None
_dp_instance = None


def get_bot() -> Bot:
    global _bot_instance
    if _bot_instance is None:
        _bot_instance = Bot(token=settings.BOT_TOKEN)
    return _bot_instance


def get_dispatcher() -> Dispatcher:
    global _dp_instance
    if _dp_instance is None:
        _dp_instance = Dispatcher()
        _dp_instance.include_router(router)
    return _dp_instance


def _user_lang(user: TelegramUser) -> str:
    return user.language or "uz"


@router.message(F.text == "/start")
async def start_handler(message: Message) -> None:
    user = await get_or_create_user(
        telegram_id=message.from_user.id,
        full_name=message.from_user.full_name or "",
        username=message.from_user.username or "",
    )
    user.state = "language"
    await sync_to_async(user.save)(update_fields=["state"])
    await message.answer(t("uz", "choose_language"), reply_markup=language_keyboard())


@router.callback_query(F.data.startswith("lang:"))
async def language_handler(callback: CallbackQuery) -> None:
    lang = callback.data.split(":")[1]
    user = await get_or_create_user(
        telegram_id=callback.from_user.id,
        full_name=callback.from_user.full_name or "",
        username=callback.from_user.username or "",
    )
    user.language = lang
    user.state = "menu"
    await sync_to_async(user.save)(update_fields=["language", "state"])
    await callback.message.answer(t(lang, "menu_title"), reply_markup=await menu_keyboard(lang))
    await callback.answer()


@router.message()
async def message_handler(message: Message) -> None:
    user = await get_or_create_user(
        telegram_id=message.from_user.id,
        full_name=message.from_user.full_name or "",
        username=message.from_user.username or "",
    )
    lang = _user_lang(user)
    text = (message.text or "").strip()

    if text == "🛒 Savat":
        await _send_cart(message, user, lang)
        return

    if text == "💳 To'lov":
        order = await create_order_from_cart(user)
        if not order:
            await message.answer(t(lang, "cart_empty"))
            return
        
        # Karta ma'lumotlarini ko'rsatish
        payment_text = t(lang, "payment_info").format(
            card_number=settings.PAYMENT_CARD_NUMBER,
            card_holder=settings.PAYMENT_CARD_HOLDER,
            amount=f"{order.total:.0f}",
            order_id=order.id,
        )
        await message.answer(t(lang, "order_created"))
        await message.answer(payment_text)
        return

    category = await sync_to_async(
        lambda: Category.objects.filter(is_active=True, name_uz=text).first()
        or Category.objects.filter(is_active=True, name_ru=text).first()
    )()
    if category:
        products = await sync_to_async(list)(
            Product.objects.filter(category=category, is_active=True).order_by("id")
        )
        if not products:
            await message.answer("Hozircha mahsulot yo'q.")
            return
        for product in products:
            name = product.name_uz if lang == "uz" else (product.name_ru or product.name_uz)
            price = f"{product.price:.2f}"
            await message.answer(
                f"{name}\nNarx: {price}",
                reply_markup=add_to_cart_keyboard(product.id),
            )
        return

    await message.answer(t(lang, "menu_title"), reply_markup=await menu_keyboard(lang))


@router.callback_query(F.data.startswith("add:"))
async def add_to_cart_handler(callback: CallbackQuery) -> None:
    product_id = int(callback.data.split(":")[1])
    product = await sync_to_async(
        Product.objects.filter(id=product_id, is_active=True).first
    )()
    if not product:
        await callback.answer("Mahsulot topilmadi.", show_alert=True)
        return
    user = await get_or_create_user(
        telegram_id=callback.from_user.id,
        full_name=callback.from_user.full_name or "",
        username=callback.from_user.username or "",
    )
    await add_to_cart(user, product, qty=1)
    await callback.answer()
    await callback.message.answer(t(_user_lang(user), "added_to_cart"))


@router.callback_query(F.data == "cart:clear")
async def cart_clear_handler(callback: CallbackQuery) -> None:
    user = await get_or_create_user(
        telegram_id=callback.from_user.id,
        full_name=callback.from_user.full_name or "",
        username=callback.from_user.username or "",
    )
    await clear_cart(user)
    await callback.answer()
    await callback.message.answer(t(_user_lang(user), "cart_cleared"))


async def _send_cart(message: Message, user: TelegramUser, lang: str) -> None:
    cart = await sync_to_async(
        lambda: user.cart_set.filter(is_active=True).prefetch_related("items__product").first()
    )()
    if not cart:
        await message.answer(t(lang, "cart_empty"))
        return
    items_count = await sync_to_async(cart.items.count)()
    if items_count == 0:
        await message.answer(t(lang, "cart_empty"))
        return
    lines = []
    total = Decimal("0")
    items = await sync_to_async(list)(cart.items.select_related("product").all())
    for item in items:
        name = item.product.name_uz if lang == "uz" else (item.product.name_ru or item.product.name_uz)
        line_total = item.product.price * item.qty
        total += line_total
        lines.append(f"{name} x{item.qty} = {line_total:.2f}")
    lines.append(f"Jami: {total:.2f}")
    await message.answer("\n".join(lines), reply_markup=cart_actions_keyboard())


def send_payment_success(telegram_id: int, lang: str = "uz") -> None:
    async def _send() -> None:
        bot = get_bot()
        await bot.send_message(chat_id=telegram_id, text=t(lang, "payment_success"))
        await bot.session.close()

    asyncio.run(_send())
