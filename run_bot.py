"""
Polling rejimida botni ishlatish (webhook kerak emas)
"""
import os
import sys
import asyncio
import django

# Django setup
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from bot.telegram import get_bot, get_dispatcher


async def main():
    bot = get_bot()
    dp = get_dispatcher()
    
    print("Bot polling rejimida ishga tushdi...")
    print("To'xtatish uchun Ctrl+C bosing")
    
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
