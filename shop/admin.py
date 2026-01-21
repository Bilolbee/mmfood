from django.contrib import admin

from .models import (
    Cart,
    CartItem,
    Category,
    Order,
    OrderItem,
    Product,
    TelegramUser,
)


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ("telegram_id", "full_name", "username", "phone", "language", "created_at")
    search_fields = ("telegram_id", "full_name", "username", "phone")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name_uz", "is_active")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name_uz", "category", "price", "is_active")
    list_filter = ("category", "is_active")


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "is_active", "created_at")


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("cart", "product", "qty")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "total", "payment_provider", "created_at")
    list_filter = ("status", "payment_provider")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "qty", "price")
