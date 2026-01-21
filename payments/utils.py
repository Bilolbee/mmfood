import base64
import json
from decimal import Decimal

from django.conf import settings

from bot.telegram import send_payment_success
from shop.models import Order


def build_click_link(order: Order) -> str | None:
    if not settings.CLICK_SERVICE_ID or not settings.CLICK_MERCHANT_ID:
        return None
    amount = f"{order.total:.2f}"
    return_url = f"{settings.SITE_URL}/payments/success/?order_id={order.id}"
    return (
        "https://my.click.uz/services/pay?"
        f"service_id={settings.CLICK_SERVICE_ID}"
        f"&merchant_id={settings.CLICK_MERCHANT_ID}"
        f"&amount={amount}"
        f"&transaction_param={order.id}"
        f"&return_url={return_url}"
    )


def build_payme_link(order: Order) -> str | None:
    if not settings.PAYME_MERCHANT_ID:
        return None
    payload = {
        "m": settings.PAYME_MERCHANT_ID,
        "ac": {"order_id": str(order.id)},
        "a": int(Decimal(order.total) * 100),
        "c": f"{settings.SITE_URL}/payments/success/?order_id={order.id}",
    }
    raw = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    token = base64.b64encode(raw).decode("utf-8")
    return f"https://checkout.paycom.uz/{token}"


def build_payment_link(order_id: int, provider: str) -> str | None:
    order = Order.objects.filter(id=order_id).first()
    if not order:
        return None
    if provider == "click":
        return build_click_link(order)
    if provider == "payme":
        return build_payme_link(order)
    return None


def mark_order_provider(order_id: int, provider: str) -> None:
    Order.objects.filter(id=order_id).update(payment_provider=provider)


def mark_order_paid(order_id: int) -> None:
    order = Order.objects.filter(id=order_id).select_related("user").first()
    if not order:
        return
    order.status = "paid"
    order.save(update_fields=["status"])
    send_payment_success(order.user.telegram_id, order.user.language or "uz")
