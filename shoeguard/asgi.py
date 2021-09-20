"""
ASGI config for shoeguard project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from os import getenv

SETTINGS = getenv("DJANGO_SECRET_KEY")

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      SETTINGS if SETTINGS else 'shoeguard.settings.dev')

application = get_asgi_application()
