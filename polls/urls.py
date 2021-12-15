from django.urls import path

from polls.views import (
    subscribe,
    task_status,
    webhook_test,
    webhook_test2,
    subscribe_ws,
    transaction_celery,
    user_subscribe
)

urlpatterns = [
    path('form/', subscribe, name='form'),
    path('task_status/', task_status, name='task_status'),
    path('webhook_test/', webhook_test, name='webhook_test'),
    path('webhook_test2/', webhook_test2, name='webhook_test2'),
    path('form_ws/', subscribe_ws, name='form_ws'),
    path('transaction_celery/', transaction_celery, name='transaction_celery'),
    path('user_subscribe/', user_subscribe, name='user_subscribe'),
]
