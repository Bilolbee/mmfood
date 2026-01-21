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
        "uz": "Buyurtma yaratildi. To'lovni amalga oshiring.",
        "ru": "Заказ создан. Пожалуйста, оплатите.",
    },
    "payment_success": {
        "uz": "To'lov muvaffaqiyatli. Buyurtma qabul qilindi.",
        "ru": "Оплата успешна. Заказ принят.",
    },
}


def t(lang: str, key: str) -> str:
    return TEXTS.get(key, {}).get(lang, TEXTS.get(key, {}).get("uz", key))
