import time
from datetime import timedelta

from DRFSHOPE.celery import app
from celery import group

from product.models import Product

app.conf.beat_schedule = {
    't1': {
        'task': 'product.tasks.t1',
        'schedule': timedelta(seconds=1),
    },
}


@app.task
def t1():
    product = Product.objects.all()
    product.delete()
