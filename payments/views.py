import json

from django.conf import settings
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .utils import mark_order_paid


def success(request: HttpRequest) -> HttpResponse:
    order_id = request.GET.get("order_id")
    if order_id:
        mark_order_paid(int(order_id))
    return render(request, "payments/success.html")


def failed(request: HttpRequest) -> HttpResponse:
    return render(request, "payments/failed.html")


@csrf_exempt
def click_callback(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        return JsonResponse({"ok": False, "detail": "Method not allowed"}, status=405)
    secret = request.headers.get("X-Secret", "")
    if settings.CLICK_SECRET_KEY and secret != settings.CLICK_SECRET_KEY:
        return JsonResponse({"ok": False, "detail": "Unauthorized"}, status=401)
    try:
        payload = json.loads(request.body.decode("utf-8"))
        order_id = int(payload.get("order_id", 0))
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({"ok": False, "detail": "Invalid payload"}, status=400)
    if order_id:
        mark_order_paid(order_id)
    return JsonResponse({"ok": True})


@csrf_exempt
def payme_callback(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        return JsonResponse({"ok": False, "detail": "Method not allowed"}, status=405)
    secret = request.headers.get("X-Secret", "")
    if settings.PAYME_SECRET_KEY and secret != settings.PAYME_SECRET_KEY:
        return JsonResponse({"ok": False, "detail": "Unauthorized"}, status=401)
    try:
        payload = json.loads(request.body.decode("utf-8"))
        order_id = int(payload.get("order_id", 0))
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({"ok": False, "detail": "Invalid payload"}, status=400)
    if order_id:
        mark_order_paid(order_id)
    return JsonResponse({"ok": True})
