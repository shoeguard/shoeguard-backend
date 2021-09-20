"""
WSGI config for shoeguard project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
from os import getenv

from django.core.wsgi import get_wsgi_application

SETTINGS = getenv("DJANGO_SECRET_KEY")

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      SETTINGS if SETTINGS else 'shoeguard.settings.dev')

application = get_wsgi_application()
