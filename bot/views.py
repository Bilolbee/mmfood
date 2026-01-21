import json

from aiogram.types import Update
from django.conf import settings
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .telegram import get_bot, get_dispatcher


@csrf_exempt
async def webhook(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        return JsonResponse({"ok": False, "detail": "Method not allowed"}, status=405)
    if settings.WEBHOOK_SECRET:
        secret = request.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
        if secret != settings.WEBHOOK_SECRET:
            return JsonResponse({"ok": False, "detail": "Unauthorized"}, status=401)
    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"ok": False, "detail": "Invalid JSON"}, status=400)

    update = Update.model_validate(data)
    bot = get_bot()
    dp = get_dispatcher()
    await dp.feed_update(bot, update)
    await bot.session.close()
    return JsonResponse({"ok": True})
from django.shortcuts import render

# Create your views here.
