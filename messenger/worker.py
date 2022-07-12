from datetime import datetime
import time

from core.broker.celery import celery_app


@celery_app.task(name="queue.test")
def test(comment_id):
    print(datetime.now())
    return True


@celery_app.task(name="queue.message")
def send_schedule_message(message, timeout):
    print(message, "asd")
    print(timeout, "delay_in_seconds")
    print(datetime.now())
    return True