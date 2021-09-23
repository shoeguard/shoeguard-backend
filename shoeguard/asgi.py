"""
ASGI config for shoeguard project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
from os import getenv

from django.core.asgi import get_asgi_application

SETTINGS = getenv("DJANGO_SETTINGS_MODULE", 'shoeguard.configs.prod')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', SETTINGS)

application = get_asgi_application()
