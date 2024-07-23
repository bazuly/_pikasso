from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pikasso.settings')

app = Celery('pikasso')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.update(
    BROKER_URL='redis://redis:6379/0',
    CELERY_RESULT_BACKEND='redis://redis:6379/0',
)

app.autodiscover_tasks()