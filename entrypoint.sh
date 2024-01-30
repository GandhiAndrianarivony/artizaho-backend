#!/bin/bash

function create_superuser() {
    echo '[INFO] Creating superuser ...'
    python3 manage.py createsuperuser --account_type E --noinput
    echo
}

function run_migration() {
    echo '[INFO] Running migration ...'
    yes | python3 manage.py makemigrations
    python3 manage.py migrate
    echo
}

function run_server() {
    python3 manage.py runserver "0.0.0.0:$1"

}

run_migration
create_superuser

run_server 8000
