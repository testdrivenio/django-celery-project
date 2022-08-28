from django.contrib.auth.models import User
from django.db import models


class Member(User):
    avatar = models.ImageField(upload_to='avatar')
    avatar_thumbnail = models.ImageField(upload_to='avatar_thumbnail', null=True, blank=True)
