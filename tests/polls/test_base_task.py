from unittest import mock

import pytest
from django.contrib.auth.models import User

from polls.factories import UserFactory
from polls.base_task import custom_celery_task


# tasks

@custom_celery_task()
def successful_task(user_pk):
    user = User.objects.get(pk=user_pk)
    user.username = 'test'
    user.save()


@custom_celery_task()
def throwing_task(user_pk):
    user = User.objects.get(pk=user_pk)
    user.username = 'test'
    user.save()
    # no retry in this task
    raise TypeError


@custom_celery_task()
def throwing_no_retry_task():
    raise TypeError


@custom_celery_task()
def throwing_retry_task():
    raise Exception


# tests

@pytest.mark.django_db()
def test_custom_celery_task(settings):
    settings.CELERY_TASK_ALWAYS_EAGER = True

    instance = UserFactory.create()
    successful_task.delay(instance.pk)

    assert User.objects.get(pk=instance.pk).username == 'test'


@pytest.mark.django_db()
def test_db_transaction(settings):
    settings.CELERY_TASK_ALWAYS_EAGER = True
    settings.CELERY_TASK_EAGER_PROPAGATES = True

    instance = UserFactory.create()

    with pytest.raises(TypeError):
        throwing_task.delay(instance.pk)

    assert User.objects.get(pk=instance.pk).username != 'test'


@pytest.mark.django_db()
def test_throwing_no_retry_task(settings):
    """
    If the exception is in EXCEPTION_BLOCK_LIST, should not retry the task
    """
    settings.CELERY_TASK_ALWAYS_EAGER = True
    settings.CELERY_TASK_EAGER_PROPAGATES = True

    with mock.patch('celery.app.task.Task.retry') as mock_retry:
        with pytest.raises(TypeError):
            throwing_no_retry_task.delay()

        mock_retry.assert_not_called()


@pytest.mark.django_db()
def test_throwing_retry_task(settings):
    settings.CELERY_TASK_ALWAYS_EAGER = True
    settings.CELERY_TASK_EAGER_PROPAGATES = True

    with mock.patch('celery.app.task.Task.retry') as mock_retry:
        with pytest.raises(Exception):
            throwing_retry_task.delay()

        mock_retry.assert_called()
        assert 'countdown' in mock_retry.call_args.kwargs
