from unittest import mock
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from faker import Faker

from tdd import tasks
from tdd.factories import MemberFactory
from tdd.models import Member


fake = Faker()


def test_get(client, db):
    response = client.get(reverse('member_signup'))
    assert response.status_code == 200


def test_post(client, db):
    fake_member = MemberFactory.build()
    password = fake.password()
    form_data = {
        'username': fake_member.username,
        'password1': password,
        'password2': password,
        'email': fake_member.email,
        'avatar': SimpleUploadedFile(
            name=fake_member.avatar.file.name,
            content=fake_member.avatar.file.read(),
            content_type='image/jpeg'),
    }

    response = client.post(reverse('member_signup'), form_data)
    assert response.status_code == 200
    assert fake_member.username in response.content.decode('utf-8')

    member = Member.objects.get(username=fake_member.username)
    assert member
    assert member.avatar


def test_post_fail(client, db):
    fake_member = MemberFactory.build()

    form_data = {
        'username': fake_member.username,
    }

    response = client.post(reverse('member_signup'), form_data)
    assert response.status_code == 200

    assert not Member.objects.count()


def test_celery_task(client, db, monkeypatch, django_capture_on_commit_callbacks):
    fake_member = MemberFactory.build()
    password = fake.password()
    form_data = {
        'username': fake_member.username,
        'password1': password,
        'password2': password,
        'email': fake_member.email,
        'avatar': SimpleUploadedFile(
            name=fake_member.avatar.file.name,
            content=fake_member.avatar.file.read(),
            content_type='image/jpeg'),
    }

    mock_generate_avatar_thumbnail_delay = mock.MagicMock(name="generate_avatar_thumbnail")
    monkeypatch.setattr(tasks.generate_avatar_thumbnail, 'delay', mock_generate_avatar_thumbnail_delay)

    with django_capture_on_commit_callbacks(execute=True) as callbacks:
        response = client.post(reverse('member_signup'), form_data)
        assert response.status_code == 200

    member = Member.objects.get(username=fake_member.username)
    assert member.pk
    mock_generate_avatar_thumbnail_delay.assert_called_with(
        member.pk
    )
