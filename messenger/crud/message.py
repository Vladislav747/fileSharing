import datetime
from sqlalchemy.orm import Session
import schemas.message as schema
from core.db.models import Message

import crud.chat_message as crud_chat_message
import crud.chat_user as crud_chat_user
import crud.chat as crud_chat
import crud.message_user as crud_message_user
import crud.message_user_readed as crud_message_user_readed

from core.broker.redis import redis


async def create_message(db: Session, message: schema.Message, user_id: int):
    """Создать сообщение и все связи"""
    result = create_message_db(db, message)
    # Добавить связку в таблицу MessageUser между пользователем и сообщением
    result_message_user = crud_message_user.create_link(db, message_id=result.id, user_id=user_id)
    # Добавить связку в таблицу MessageChat между чатом и сообщением
    result_chat_message = crud_chat_message.create_link(db, chat_id=message.chat_id, message_id=result.id)
    # Добавить связку в таблицу UserChat между чатом и сообщением
    result_chat_message = crud_chat_user.create_link(db, chat_id=message.chat_id, user_id=user_id)
    # Добавить обновление для last_message для  чата
    result_chat_message = crud_chat.update_last_time_chat(db, chat_id=message.chat_id)
    # Добавить связку для  для  чата для статуса message_is_readed
    crud_message_user_readed.create_message_user_read(db, message_id=result.id, chat_id=message.chat_id)
    # Известить вебсокет о новых сообщениях
    await redis.publish(f"chat-{message.chat_id}", message.message)
    return result

def create_message_db(db: Session, message: schema.Message):
    """Создать сообщение"""
    message_db = Message(message=message.message)
    db.add(message_db)
    db.commit()

    return message_db


def get_all_messages(db: Session):
    """Получить все сообщения"""
    return db.query(Message).all()


def get_message_by_id(db: Session, message_id: int):
    """Получить сообщение по id"""
    return db.query(Message).filter(Message.id == message_id).one_or_none()


def delete_message(db: Session, message_id: int):
    """Удалить сообщение"""
    db.query(Message).filter(Message.id == message_id).delete()
    db.commit()


def update_message(db: Session, message: schema.Message):
    """Обновить данные сообщение"""
    message_db = db.query(Message).filter(Message.id == message.id).one_or_none()
    for param, value in message.dict().items():
        if value is not None:
            setattr(message_db, param, value)
    # Обновить update_date время сообщения
    setattr(message_db, "updated_date", datetime.datetime.now())
    setattr(message_db, "changed", True)
    db.commit()

    return message_db