TEXTS = {
    "choose_language": {
        "uz": "Tilni tanlang:",
        "ru": "Выберите язык:",
    },
    "menu_title": {
        "uz": "Kategoriya tanlang yoki savat/to'lov bo'limiga o'ting.",
        "ru": "Выберите категорию или перейдите в корзину/оплату.",
    },
    "cart_empty": {
        "uz": "Savat bo'sh.",
        "ru": "Корзина пуста.",
    },
    "added_to_cart": {
        "uz": "Savatga qo'shildi.",
        "ru": "Добавлено в корзину.",
    },
    "cart_cleared": {
        "uz": "Savat tozalandi.",
        "ru": "Корзина очищена.",
    },
    "choose_payment": {
        "uz": "To'lov turini tanlang:",
        "ru": "Выберите способ оплаты:",
    },
    "order_created": {
        "uz": "📦 Buyurtma yaratildi!",
        "ru": "📦 Заказ создан!",
    },
    "payment_info": {
        "uz": "💳 To'lov uchun pul o'tkazing:\n\n💳 Karta: {card_number}\n👤 Ism: {card_holder}\n💰 Summa: {amount} so'm\n📝 Buyurtma: #{order_id}\n\n✅ Pul o'tkazgach, screenshot yuboring yoki admin bilan bog'laning.\n📱 Telefon: +998 90 123 45 67",
        "ru": "💳 Переведите деньги:\n\n💳 Карта: {card_number}\n👤 Имя: {card_holder}\n💰 Сумма: {amount} сум\n📝 Заказ: #{order_id}\n\n✅ После оплаты отправьте скриншот или свяжитесь с админом.\n📱 Телефон: +998 90 123 45 67",
    },
    "payment_success": {
        "uz": "✅ To'lov muvaffaqiyatli! Buyurtma qabul qilindi.",
        "ru": "✅ Оплата успешна! Заказ принят.",
    },
}


def t(lang: str, key: str) -> str:
    return TEXTS.get(key, {}).get(lang, TEXTS.get(key, {}).get("uz", key))
