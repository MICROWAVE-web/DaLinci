worker: ps:scale web=1 worker=5
web: gunicorn DaLinci.wsgi --log-file -
release: python manage.py migrate