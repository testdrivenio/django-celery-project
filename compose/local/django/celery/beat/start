#!/bin/bash

set -o errexit
set -o nounset

rm -f './celerybeat.pid'
celery -A django_celery_example beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler