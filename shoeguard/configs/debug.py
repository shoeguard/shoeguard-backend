from os import getenv

from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-q5n4(&ogy*gbw@pj#7+@pjwulg6sd9*l1(m$6m(bibu%x@vhr7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'shoeguard',
        'USER': 'shoeguard',
        'HOST': "db" if getenv("IS_DOCKER") == "true" else '127.0.0.1',
        'PORT': 5432,
    }
}
