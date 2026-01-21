from django.core.management.base import BaseCommand

from shop.models import Category, Product


class Command(BaseCommand):
    help = "Initialize sample data"

    def handle(self, *args, **options):
        # Categories
        lavash, _ = Category.objects.get_or_create(
            name_uz='🌯 Lavashlar',
            defaults={'name_ru': '🌯 Лаваши', 'is_active': True}
        )
        somsa, _ = Category.objects.get_or_create(
            name_uz='🥟 Somsalar',
            defaults={'name_ru': '🥟 Самсы', 'is_active': True}
        )
        burger, _ = Category.objects.get_or_create(
            name_uz='🍔 Burgerlar',
            defaults={'name_ru': '🍔 Бургеры', 'is_active': True}
        )
        pitsa, _ = Category.objects.get_or_create(
            name_uz='🍕 Pitsalar',
            defaults={'name_ru': '🍕 Пиццы', 'is_active': True}
        )
        garnir, _ = Category.objects.get_or_create(
            name_uz='🍟 Garnirlar',
            defaults={'name_ru': '🍟 Гарниры', 'is_active': True}
        )
        drink, _ = Category.objects.get_or_create(
            name_uz='🥤 Ichimliklar',
            defaults={'name_ru': '🥤 Напитки', 'is_active': True}
        )

        # Lavashlar
        Product.objects.get_or_create(
            category=lavash, name_uz='Tovuqli lavash',
            defaults={'name_ru': 'Куриный лаваш', 'price': 25000, 'is_active': True}
        )
        Product.objects.get_or_create(
            category=lavash, name_uz="Go'shtli lavash",
            defaults={'name_ru': 'Мясной лаваш', 'price': 28000, 'is_active': True}
        )
        Product.objects.get_or_create(
            category=lavash, name_uz='Tandir lavash',
            defaults={'name_ru': 'Тандырный лаваш', 'price': 30000, 'is_active': True}
        )
        Product.objects.get_or_create(
            category=lavash, name_uz='Sirli lavash',
            defaults={'name_ru': 'Сырный лаваш', 'price': 27000, 'is_active': True}
        )
        Product.objects.get_or_create(
            category=lavash, name_uz='Qazi lavash',
            defaults={'name_ru': 'Казы лаваш', 'price': 32000, 'is_active': True}
        )

        # Somsalar
        Product.objects.get_or_create(
            category=somsa, name_uz="Go'shtli somsa",
            defaults={'name_ru': 'Мясная самса', 'price': 8000, 'is_active': True}
        )
        Product.objects.get_or_create(
            category=somsa, name_uz='Kartoshkali somsa',
            defaults={'name_ru': 'Картофельная самса', 'price': 6000, 'is_active': True}
        )
        Product.objects.get_or_create(
            category=somsa, name_uz='Qovoqli somsa',
            defaults={'name_ru': 'Тыквенная самса', 'price': 7000, 'is_active': True}
        )
        Product.objects.get_or_create(
            category=somsa, name_uz='Sirli somsa',
            defaults={'name_ru': 'Сырная самса', 'price': 9000, 'is_active': True}
        )

        # Burgerlar
        Product.objects.get_or_create(
            category=burger, name_uz='Gamburger',
            defaults={'name_ru': 'Гамбургер', 'price': 22000, 'is_active': True}
        )
        Product.objects.get_or_create(
            category=burger, name_uz='Chizburger',
            defaults={'name_ru': 'Чизбургер', 'price': 25000, 'is_active': True}
        )
        Product.objects.get_or_create(
            category=burger, name_uz='Tovuq burger',
            defaults={'name_ru': 'Куриный бургер', 'price': 24000, 'is_active': True}
        )
        Product.objects.get_or_create(
            category=burger, name_uz='Big Burger',
            defaults={'name_ru': 'Биг Бургер', 'price': 35000, 'is_active': True}
        )

        # Pitsalar
        Product.objects.get_or_create(
            category=pitsa, name_uz='Margarita',
            defaults={'name_ru': 'Маргарита', 'price': 45000, 'is_active': True}
        )
        Product.objects.get_or_create(
            category=pitsa, name_uz='Pepperoni',
            defaults={'name_ru': 'Пепперони', 'price': 50000, 'is_active': True}
        )
        Product.objects.get_or_create(
            category=pitsa, name_uz='Tovuqli pitsa',
            defaults={'name_ru': 'Куриная пицца', 'price': 48000, 'is_active': True}
        )
        Product.objects.get_or_create(
            category=pitsa, name_uz='4 pishloqli',
            defaults={'name_ru': '4 сыра', 'price': 55000, 'is_active': True}
        )

        # Garnirlar
        Product.objects.get_or_create(
            category=garnir, name_uz='Free kartoshka',
            defaults={'name_ru': 'Картофель фри', 'price': 12000, 'is_active': True}
        )
        Product.objects.get_or_create(
            category=garnir, name_uz='Kartoshka po-derevenski',
            defaults={'name_ru': 'Картофель по-деревенски', 'price': 15000, 'is_active': True}
        )
        Product.objects.get_or_create(
            category=garnir, name_uz='Hot-dog',
            defaults={'name_ru': 'Хот-дог', 'price': 18000, 'is_active': True}
        )
        Product.objects.get_or_create(
            category=garnir, name_uz='Sezar salat',
            defaults={'name_ru': 'Салат Цезарь', 'price': 20000, 'is_active': True}
        )

        # Ichimliklar
        Product.objects.get_or_create(
            category=drink, name_uz='Coca-Cola 0.5L',
            defaults={'name_ru': 'Кока-Кола 0.5Л', 'price': 8000, 'is_active': True}
        )
        Product.objects.get_or_create(
            category=drink, name_uz='Fanta 0.5L',
            defaults={'name_ru': 'Фанта 0.5Л', 'price': 8000, 'is_active': True}
        )
        Product.objects.get_or_create(
            category=drink, name_uz='Sprite 0.5L',
            defaults={'name_ru': 'Спрайт 0.5Л', 'price': 8000, 'is_active': True}
        )
        Product.objects.get_or_create(
            category=drink, name_uz='Suv 0.5L',
            defaults={'name_ru': 'Вода 0.5Л', 'price': 3000, 'is_active': True}
        )
        Product.objects.get_or_create(
            category=drink, name_uz='Choy',
            defaults={'name_ru': 'Чай', 'price': 5000, 'is_active': True}
        )
        Product.objects.get_or_create(
            category=drink, name_uz='Kofe',
            defaults={'name_ru': 'Кофе', 'price': 10000, 'is_active': True}
        )

        self.stdout.write(self.style.SUCCESS(f'Categories: {Category.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Products: {Product.objects.count()}'))
