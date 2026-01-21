release: python manage.py migrate && python manage.py init_data
web: gunicorn config.asgi:application -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT --timeout 120
