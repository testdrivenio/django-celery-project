from factory import LazyAttribute
from factory.django import DjangoModelFactory, ImageField
from factory import Faker

from django.contrib.auth.hashers import make_password
from tdd.models import Member


class MemberFactory(DjangoModelFactory):
    class Meta:
        model = Member

    username = Faker("user_name")
    email = LazyAttribute(lambda o: '%s@example.com' % o.username)
    password = LazyAttribute(lambda o: make_password(o.username))
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    avatar = ImageField(width=1000, height=1000)
