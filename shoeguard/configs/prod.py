from os import getenv

from dotenv import load_dotenv

from .base import *

load_dotenv()

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = getenv("DJANGO_SECRET_KEY")
if SECRET_KEY is None or SECRET_KEY == "":
    SECRET_KEY = "707m!rpdzi2ta8jv6$y2fwjx@j1%o^02+45%1o=r%jm$m8oma!"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'shoeguard',
        'USER': 'shoeguard',
        'HOST': 'db',
        'PORT': 5432,
    }
}
