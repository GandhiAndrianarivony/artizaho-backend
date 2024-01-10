#!/bin/bash

python /apps/manage.py makemigrations
python /apps/manage.py migrate
# python /apps/manage.py createsuperuser --type P --gender M --dob '2000-12-12' --noinput
python /apps/manage.py runserver 0.0.0.0:8000