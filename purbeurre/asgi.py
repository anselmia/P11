"""
ASGI config for purbeurre project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""
# pragma: no cover
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "purbeurre.settings"
)  # pragma: no cover

application = get_asgi_application()  # pragma: no cover
