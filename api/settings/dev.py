""""configuration of develop"""


import environ

from .base import *


env = environ.Env(
    DEBUG=(bool, False)
)
# environ.Env.read_env(BASE_DIR / "dev.env")

SECRET_KEY = env("SECRET_KEY")

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

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:9237",
    "http://localhost:9237"
]
