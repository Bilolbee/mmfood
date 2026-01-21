from django.db import models


class TelegramUser(models.Model):
    telegram_id = models.BigIntegerField(unique=True)
    full_name = models.CharField(max_length=255, blank=True)
    username = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=32, blank=True)
    language = models.CharField(
        max_length=5, choices=[("uz", "Uz"), ("ru", "Ru")], blank=True
    )
    state = models.CharField(max_length=32, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.telegram_id} {self.full_name}".strip()


class Category(models.Model):
    name_uz = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name_uz


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    name_uz = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name_uz


class Cart(models.Model):
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("cart", "product")


class Order(models.Model):
    STATUS_CHOICES = [
        ("new", "New"),
        ("pending_payment", "Pending payment"),
        ("paid", "Paid"),
        ("preparing", "Preparing"),
        ("delivering", "Delivering"),
        ("done", "Done"),
        ("canceled", "Canceled"),
    ]
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default="new")
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    payment_provider = models.CharField(
        max_length=16, choices=[("click", "Click"), ("payme", "Payme")], blank=True
    )
    payment_id = models.CharField(max_length=128, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Order {self.id} {self.user.telegram_id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2)
