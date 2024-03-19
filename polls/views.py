import json
import logging
import random
import time
from functools import partial

import requests
from celery.result import AsyncResult
from django.contrib.auth.models import User
from django.db import transaction
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from string import ascii_lowercase

from polls.forms import YourForm
from polls.tasks import (
    sample_task,
    task_process_notification,
    task_send_welcome_email,
    task_add_subscribe,
)


logger = logging.getLogger(__name__)


# helpers
def random_username():
    username = ''.join([random.choice(ascii_lowercase) for i in range(5)])
    return username


def api_call(email):
    # used for testing a failed api call
    if random.choice([0, 1]):
        raise Exception('random processing error')

    # used for simulating a call to a third-party api
    requests.post('https://httpbin.org/delay/5')


# views

def subscribe(request):
    if request.method == 'POST':
        form = YourForm(request.POST)
        if form.is_valid():
            task = sample_task.delay(form.cleaned_data['email'])
            # return the task id so the JS can poll the state
            return JsonResponse({
                'task_id': task.task_id,
            })

    form = YourForm()
    return render(request, 'form.html', {'form': form})


def task_status(request):
    task_id = request.GET.get('task_id')

    if task_id:
        task = AsyncResult(task_id)
        state = task.state

        if state == 'FAILURE':
            error = str(task.result)
            response = {
                'state': state,
                'error': error,
            }
        else:
            response = {
                'state': state,
            }
        return JsonResponse(response)


@csrf_exempt
def webhook_test(request):
    if not random.choice([0, 1]):
        # mimic an error
        raise Exception()

    # blocking process
    requests.post('https://httpbin.org/delay/5')
    return HttpResponse('pong')


@csrf_exempt
def webhook_test_async(request):
    """
    Use celery worker to handle the notification
    """
    task = task_process_notification.delay()
    logger.info(task.id)
    return HttpResponse('pong')


def subscribe_ws(request):
    """
    Use Websocket to get notification of Celery task, instead of using ajax polling
    """
    if request.method == 'POST':
        form = YourForm(request.POST)
        if form.is_valid():
            task = sample_task.delay(form.cleaned_data['email'])
            # return the task id so the JS can poll the state
            return JsonResponse({
                'task_id': task.task_id,
            })

    form = YourForm()
    return render(request, 'form_ws.html', {'form': form})


@transaction.atomic
def transaction_celery(request):
    username = random_username()
    user = User.objects.create_user(username, 'lennon@thebeatles.com', 'johnpassword')
    logger.info(f'create user {user.pk}')
    # the task does not get called until after the transaction is committed
    transaction.on_commit(partial(task_send_welcome_email.delay, user.pk))

    time.sleep(1)
    return HttpResponse('test')


@transaction.atomic
def user_subscribe(request):
    """
    This Django view saves user info to the db and sends task to Celery worker
    to subscribe the user to the database
    """
    if request.method == 'POST':
        form = YourForm(request.POST)
        if form.is_valid():
            instance, flag = User.objects.get_or_create(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
            )
            transaction.on_commit(
                partial(task_add_subscribe.delay, instance.pk)
            )
            return HttpResponseRedirect('')
    else:
        form = YourForm()

    return render(request, 'user_subscribe.html', {'form': form})
