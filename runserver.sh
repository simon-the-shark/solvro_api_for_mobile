#!/bin/sh

python manage.py collectstatic --no-input
python manage.py migrate
gunicorn solvro_api_for_mobile.wsgi --bind=0.0.0.0:80