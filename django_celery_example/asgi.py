import os

import django
from asgiref.compatibility import guarantee_single_callable
from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf import settings

from polls import routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_celery_example.settings')
django.setup()

application = ProtocolTypeRouter({
    'websocket': URLRouter(
        routing.urlpatterns
    )
})

if not settings.DEBUG:
    # https://github.com/django/channels/issues/1319
    application = guarantee_single_callable(application)
