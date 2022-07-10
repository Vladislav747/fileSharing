import datetime
from sqlalchemy.orm import Session
from core.db.models import MessageUserRead, MessageUser, ChatMessage
import crud.chat_user as crud_chat_user


def create_message_user_read(db: Session, message_id: int, chat_id: int):
    """Создать метка null по умолчанию для сообщения о прочтении"""

    # Нужно для каждого пользователя создать метку о том что пользователь прочитал сообщение
    # Поэтому сначала нужно определить всех пользователей в чате
    users_in_chat = crud_chat_user.get_all_users_in_chat(db, chat_id=chat_id)
    # И для каждого пользователя создать метку
    for value in users_in_chat:
        user_id = value._asdict().get('user_id')
        message_db = MessageUserRead(user_id=user_id, message_id=message_id, message_is_read=False)
        db.add(message_db)
        db.commit()

    return message_db


def get_all_readed_messages_in_chat(db: Session, user_id: int, chat_id: int):
    """Получить все метки о прочтении сообщение о пользователе в определенном чате"""
    return db.query(MessageUserRead).join(ChatMessage, MessageUserRead.message_id == ChatMessage.message_id).filter(MessageUserRead.user_id == user_id, ChatMessage.chat_id == chat_id).all()


def delete_message_user_read(db: Session, message_id: int, user_id: int):
    """Удалить сообщение """
    db.query(MessageUserRead).filter(
        MessageUserRead.message_id == message_id,
        MessageUserRead.user_id == user_id
    ).delete()

    db.commit()


def update_message(db: Session, user_id: int, chat_id: int):
    """Проставить метки о прочтении(прочтено) для всех сообщений в определенном чате"""
    message_db = db.query(MessageUserRead).filter(Message.chat_id == message.chat_id).one_or_none()
    for param, value in message.dict().items():
        if value is not None:
            setattr(message_db, param, value)
    # Обновить update_date время сообщения
    setattr(message_db, "updated_date", datetime.datetime.now())
    setattr(message_db, "changed", True)
    db.commit()

    return message_db