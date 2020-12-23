import shlex
import sys
import subprocess

from django.core.management.base import BaseCommand
from django.utils import autoreload


def restart_celery():
    cmd = 'pkill -f "celery worker"'
    if sys.platform == 'win32':
        cmd = 'taskkill /f /t /im celery.exe'

    subprocess.call(shlex.split(cmd))
    subprocess.call(shlex.split('celery worker -A django_celery_example --loglevel=info'))


class Command(BaseCommand):

    def handle(self, *args, **options):
        print('Starting celery worker with autoreload...')
        autoreload.run_with_reloader(restart_celery)
