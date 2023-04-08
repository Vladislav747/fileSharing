from datetime import datetime
import asyncio

from app.broker.celery import celery_app
import crud.message as crud
from app.db.session import session
from schemas.message import Message


@celery_app.task(name="queue.test")
def test(comment_id):
    print(datetime.now())
    return True


@celery_app.task(name="queue.message")
def send_schedule_message(message: str, user_id: int, chat_id: int):
    db = session()
    async_func = crud.create_message(db, message=Message(chat_id=chat_id, message=message), user_id=user_id)
    asyncio.run(async_func)

    return True