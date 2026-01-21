import asyncio

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from bot.telegram import get_bot


class Command(BaseCommand):
    help = "Set Telegram webhook"

    def handle(self, *args, **options):
        if not settings.WEBHOOK_URL:
            raise CommandError("WEBHOOK_URL is not set")

        async def _run() -> None:
            bot = get_bot()
            await bot.set_webhook(
                url=settings.WEBHOOK_URL,
                secret_token=settings.WEBHOOK_SECRET or None,
            )
            await bot.session.close()

        asyncio.run(_run())
        self.stdout.write(self.style.SUCCESS("Webhook set"))
