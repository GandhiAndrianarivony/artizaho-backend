#!/bin/bash


yes | python /apps/manage.py makemigrations
python /apps/manage.py migrate

# CREATE ADMIN USER
create_super_user=$(python /apps/manage.py createsuperuser  --first_name artizaho_fn --last_name artizaho_ln --type P --gender M --dob '2000-12-12' --noinput 2>&1)
status=$? # Capture the exit command
if [[ $status -eq 1 ]]; then
    echo "================================================================"
    echo "[INFO] User already existed ⚠️"
    echo "================================================================"
fi

# RUN SERVER
python /apps/manage.py runserver 0.0.0.0:8000