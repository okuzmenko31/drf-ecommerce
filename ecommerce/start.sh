#!/bin/sh

sleep 10
python /drf_ecommerce/apps/manage.py makemigrations
python /drf_ecommerce/apps/manage.py migrate
python /drf_ecommerce/apps/manage.py runserver 0.0.0.0:8000
python /drf_ecommerce/apps/manage.py collectstatic
