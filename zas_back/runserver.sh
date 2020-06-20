#!/bin/bash

cd zas_back

python manage.py migrate --noinput
python manage.py bootstrap_admin
gunicorn -k uvicorn.workers.UvicornWorker zas_back.asgi:application