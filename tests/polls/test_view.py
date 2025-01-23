from unittest import mock

from django.contrib.auth.models import User
from django.urls import reverse

from polls import tasks


def test_subscribe_post_succeed(db, monkeypatch, client, user, django_capture_on_commit_callbacks):
    mock_task_add_subscribe_delay = mock.MagicMock(name="task_add_subscribe_delay")
    monkeypatch.setattr(tasks.task_add_subscribe, 'delay', mock_task_add_subscribe_delay)

    with django_capture_on_commit_callbacks(execute=True) as callbacks:
        response = client.post(
            reverse('user_subscribe'),
            {
                'username': user.username,
                'email': user.email,
            }
        )

    assert response.status_code == 302
    assert User.objects.filter(username=user.username).exists() is True

    user = User.objects.filter(username=user.username).first()
    mock_task_add_subscribe_delay.assert_called_with(
        user.pk
    )
