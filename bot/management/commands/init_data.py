from django.core.management.base import BaseCommand

from shop.models import Category, Product


class Command(BaseCommand):
    help = "Initialize sample data"

    def handle(self, *args, **options):
        # Categories
        c1, _ = Category.objects.get_or_create(
            name_uz='🍕 Pitsa',
            defaults={'name_ru': '🍕 Пицца', 'is_active': True}
        )
        c2, _ = Category.objects.get_or_create(
            name_uz='🍔 Burger',
            defaults={'name_ru': '🍔 Бургер', 'is_active': True}
        )
        c3, _ = Category.objects.get_or_create(
            name_uz='🥤 Ichimliklar',
            defaults={'name_ru': '🥤 Напитки', 'is_active': True}
        )

        # Products
        Product.objects.get_or_create(
            category=c1, name_uz='Margarita',
            defaults={'name_ru': 'Маргарита', 'price': 35000, 'is_active': True}
        )
        Product.objects.get_or_create(
            category=c1, name_uz='Pepperoni',
            defaults={'name_ru': 'Пепперони', 'price': 42000, 'is_active': True}
        )
        Product.objects.get_or_create(
            category=c2, name_uz='Cheeseburger',
            defaults={'name_ru': 'Чизбургер', 'price': 28000, 'is_active': True}
        )
        Product.objects.get_or_create(
            category=c2, name_uz='Big Burger',
            defaults={'name_ru': 'Биг Бургер', 'price': 38000, 'is_active': True}
        )
        Product.objects.get_or_create(
            category=c3, name_uz='Coca Cola',
            defaults={'name_ru': 'Кока Кола', 'price': 8000, 'is_active': True}
        )
        Product.objects.get_or_create(
            category=c3, name_uz='Fanta',
            defaults={'name_ru': 'Фанта', 'price': 8000, 'is_active': True}
        )

        self.stdout.write(self.style.SUCCESS(f'Categories: {Category.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Products: {Product.objects.count()}'))
