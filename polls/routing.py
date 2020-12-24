from django.conf.urls import url

from polls import consumers


urlpatterns = [
    url(r'^ws/task_status/(?P<task_id>[\w-]+)/?$', consumers.TaskStatusConsumer.as_asgi()),
]
