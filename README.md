# MMFood Telegram Bot (Django + aiogram)

Professional Telegram bot for menu → cart → payment flow with Click/Payme and Django admin.

## Quick Start (Lokal test - Polling rejimi)

1) Virtual environment yarating
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2) `.env` faylni yarating
```powershell
copy env.example .env
notepad .env
```
`.env` ichida `BOT_TOKEN=` qatoriga tokenni qo'ying (chatga yozmang!)

3) Ma'lumotlar bazasini tayyorlang
```powershell
python manage.py migrate
python manage.py createsuperuser
```

4) Admin panelga Category va Product qo'shing
```powershell
python manage.py runserver
```
Brauzerda: `http://localhost:8000/admin/`

5) Botni ishga tushiring (polling)
```powershell
python run_bot.py
```

Tayyor! Botni Telegram'da sinab ko'ring.

---

## Production (Webhook rejimi)

1-3 qadamlar bir xil

4) `.env` ichida webhook sozlang
```
WEBHOOK_URL=https://your-domain.com/bot/webhook/
SITE_URL=https://your-domain.com
```

5) Set webhook
```
python manage.py set_webhook
```

## Click/Payme Callbacks
Set provider webhooks to:
- `https://your-domain.com/payments/click/callback/`
- `https://your-domain.com/payments/payme/callback/`

The current callbacks are minimal and expect JSON:
```
{ "order_id": 123 }
```
and `X-Secret` header matching `CLICK_SECRET_KEY` or `PAYME_SECRET_KEY`.

## Deploy (Ubuntu + Nginx + Gunicorn)
1) Install requirements: `python3-venv`, `nginx`
2) Clone project, create `.env`
3) Install deps and migrate:
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic
```
4) Gunicorn:
```
pip install gunicorn
gunicorn config.wsgi:application --bind 127.0.0.1:8000
```
5) Nginx reverse proxy to 127.0.0.1:8000
6) HTTPS (Let’s Encrypt) and set `WEBHOOK_URL`

## Deploy (Render - Free)
1) Push code to GitHub
2) Render → New Web Service → select repo
3) Use these commands:
   - Build: `pip install -r requirements.txt`
   - Start: `python manage.py migrate && gunicorn config.asgi:application -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`
4) Set env vars in Render:
   - `BOT_TOKEN` (do not share)
   - `WEBHOOK_SECRET`
   - `WEBHOOK_URL` = `https://<render-app>.onrender.com/bot/webhook/`
   - `SITE_URL` = `https://<render-app>.onrender.com`
5) After deploy, run `python manage.py set_webhook` (Render shell or local with same env)
