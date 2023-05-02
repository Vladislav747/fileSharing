import os
import time

from celery import Celery

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379")


@celery.task(name="create_task")
def create_task():
    print("create_task")
    # time.sleep(int(12) * 10)
    return True
