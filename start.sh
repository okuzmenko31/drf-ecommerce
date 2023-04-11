#!/bin/sh

sleep 10
python /app/ecommerce/ecommerce/manage.py makemigrations
python /app/ecommerce/ecommerce/manage.py migrate
python /app/ecommerce/ecommerce/manage.py runserver 0.0.0.0:8000
python /app/ecommerce/ecommerce/manage.py collectstatic
