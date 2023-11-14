"""
ASGI config for shoppinglist project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""
# INFOKAN DEPLOY ULANG
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shoppinglist.settings')

application = get_asgi_application()
