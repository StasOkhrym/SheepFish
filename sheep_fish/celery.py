import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sheep_fish.settings")

app = Celery("sheep_fish")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
