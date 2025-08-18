from datetime import timedelta

from celery import Celery
import os
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DRFSHOPE.settings')
app = Celery('DRFSHOPE')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
