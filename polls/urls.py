from django.urls import path

from polls.views import (
    form,
    task_status,
    webhook_test,
    webhook_test2,
    form_ws,
    transaction_celery,
    subscribe,
)


urlpatterns = [
    path('form/', form, name='form'),
    path('task_status/', task_status, name='task_status'),
    path('webhook_test/', webhook_test, name='webhook_test'),
    path('webhook_test2', webhook_test2, name='webhook_test2'),
    path('form_ws/', form_ws, name='form_ws'),
    path('transaction_celery/', transaction_celery, name='transaction_celery'),
    path('subscribe/', subscribe, name='subscribe'),
]
