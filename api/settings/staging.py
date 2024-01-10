"""Contains configuration of staging
"""

import environ

from .base import *


env = environ.Env()
environ.Env.read_env(BASE_DIR / "staging.env")

SECRET_KEY = env("SECRET_KEY")

DEBUG = False

DATABASES = {
    'default': {
        **{
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
        }, 
        **{
            "NAME": env("POSTGRES_DB"),
            "USER": env("POSTGRES_USER"),
            "PASSWORD": env("POSTGRES_PASSWORD"),
            "HOST": env("DB_HOST"),
            "PORT": env("DB_PORT"),
            'DJANGO_SETTINGS_MODULE': env("DJANGO_SETTINGS_MODULE")
        }
    }
}
