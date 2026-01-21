from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from asgiref.sync import sync_to_async

from shop.models import Category


def language_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🇺🇿 O'zbek", callback_data="lang:uz"),
                InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang:ru"),
            ]
        ]
    )


async def menu_keyboard(language: str) -> ReplyKeyboardMarkup:
    categories = await sync_to_async(list)(
        Category.objects.filter(is_active=True).order_by("id")
    )
    rows = []
    row = []
    for category in categories:
        name = category.name_uz if language == "uz" else (category.name_ru or category.name_uz)
        row.append(KeyboardButton(text=name))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    rows.append([KeyboardButton(text="🛒 Savat"), KeyboardButton(text="💳 To'lov")])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)


def add_to_cart_keyboard(product_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➕ Savatga", callback_data=f"add:{product_id}")]
        ]
    )


def cart_actions_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🧹 Savatni tozalash", callback_data="cart:clear")]
        ]
    )
