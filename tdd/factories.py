from django.contrib.auth.hashers import make_password
from factory import LazyAttribute
from factory.django import DjangoModelFactory, ImageField
from factory.fuzzy import FuzzyText

from tdd.models import Member


class MemberFactory(DjangoModelFactory):
    class Meta:
        model = Member

    username = FuzzyText(length=6)
    email = LazyAttribute(lambda o: '%s@example.com' % o.username)
    password = LazyAttribute(lambda o: make_password(o.username))
    first_name = FuzzyText(length=6)
    last_name = FuzzyText(length=6)
    avatar = ImageField(width=1000, height=1000)
