from __future__ import absolute_import, unicode_literals

import os
from datetime import timedelta

from celery import Celery
from django.conf import settings
from kombu import Queue

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "library_management.settings")

app = Celery("library_management")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.task_queues = (
    Queue("default"),
    Queue("mailing"),
    Queue("low_priority"),
    Queue("high_priority"),
)

app.conf.beat_schedule = {
    "test": {
        "task": "library_management.tasks.test_task",
        "schedule": timedelta(seconds=2),
        "args": (),
        "options": {
            "expires": 10,
            "queue": "low_priority",
        },
    },
}
app.conf.task_routes = {}
app.conf.task_default_queue = "default"


app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
