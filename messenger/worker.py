from datetime import datetime

from core.broker.celery import celery_app


@celery_app.task(name="queue.test")
def test(comment_id):
    print(comment_id, "asd")
    print(datetime.now())
    return True