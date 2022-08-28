"""
ASGI config for django_celery_example project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from polls import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_celery_example.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket': URLRouter(
        routing.urlpatterns
    )
})

