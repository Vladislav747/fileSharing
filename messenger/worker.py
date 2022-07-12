from datetime import datetime

from core.broker.celery import celery_app


@celery_app.task(name="queue.test")
def test(comment_id):
    print(datetime.now())
    return True


@celery_app.task(name="queue.message")
def send_schedule_message(message: str, user_id: int, chat_id: int):
    print(message, "message")
    print(user_id, "user_id")
    print(chat_id, "chat_id")

    return True