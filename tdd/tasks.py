from io import BytesIO

from celery import shared_task
from django.core.files import File
from PIL import Image

from tdd.models import Member


@shared_task(name='generate_avatar_thumbnail')
def generate_avatar_thumbnail(member_pk):
    member = Member.objects.get(pk=member_pk)

    im = Image.open(member.avatar)
    size = (100, 100)
    im.thumbnail(size)
    thumb_io = BytesIO()
    im.save(thumb_io, 'JPEG')

    member.avatar_thumbnail = File(thumb_io, name=f'{member.pk}-avatar-thumbnail.jpg')
    member.save(update_fields=["avatar_thumbnail"])
