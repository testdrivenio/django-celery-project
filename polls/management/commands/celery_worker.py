import shlex
import subprocess
import sys

from django.core.management.base import BaseCommand
from django.utils import autoreload


def restart_celery():
    celery_worker_cmd = "celery -A django_celery_example worker"
    cmd = f'pkill -f "{celery_worker_cmd}"'
    if sys.platform == "win32":
        cmd = "taskkill /f /t /im celery.exe"

    subprocess.call(shlex.split(cmd))
    subprocess.call(shlex.split(f"{celery_worker_cmd} --loglevel=info -Q high_priority,default"))


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Starting celery worker with autoreload...")
        autoreload.run_with_reloader(restart_celery)
