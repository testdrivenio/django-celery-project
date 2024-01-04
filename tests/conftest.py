import pytest
from factory import LazyAttribute
from factory.django import DjangoModelFactory
from factory import Faker

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from pytest_factoryboy import register
from polls.factories import UserFactory

register(UserFactory)
