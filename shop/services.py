from decimal import Decimal

from .models import Cart, CartItem, Order, OrderItem, Product, TelegramUser


def get_or_create_user(telegram_id: int, full_name: str, username: str) -> TelegramUser:
    user, _created = TelegramUser.objects.get_or_create(
        telegram_id=telegram_id,
        defaults={"full_name": full_name, "username": username},
    )
    if full_name and user.full_name != full_name:
        user.full_name = full_name
    if username and user.username != username:
        user.username = username
    user.save(update_fields=["full_name", "username"])
    return user


def get_active_cart(user: TelegramUser) -> Cart:
    cart, _created = Cart.objects.get_or_create(user=user, is_active=True)
    return cart


def add_to_cart(user: TelegramUser, product: Product, qty: int = 1) -> CartItem:
    cart = get_active_cart(user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if created:
        item.qty = qty
    else:
        item.qty += qty
    item.save()
    return item


def clear_cart(user: TelegramUser) -> None:
    Cart.objects.filter(user=user, is_active=True).delete()


def cart_total(cart: Cart) -> Decimal:
    total = Decimal("0")
    for item in cart.items.select_related("product"):
        total += item.product.price * item.qty
    return total


def create_order_from_cart(user: TelegramUser) -> Order | None:
    cart = Cart.objects.filter(user=user, is_active=True).prefetch_related(
        "items__product"
    ).first()
    if not cart or cart.items.count() == 0:
        return None
    total = cart_total(cart)
    order = Order.objects.create(user=user, total=total, status="pending_payment")
    order_items = [
        OrderItem(
            order=order,
            product=item.product,
            qty=item.qty,
            price=item.product.price,
        )
        for item in cart.items.all()
    ]
    OrderItem.objects.bulk_create(order_items)
    cart.is_active = False
    cart.save(update_fields=["is_active"])
    return order
