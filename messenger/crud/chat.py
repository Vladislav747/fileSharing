from datetime import datetime
from enum import Enum
import schemas.chat as schema
from core.db.models import Chat
from sqlalchemy.orm import Session


class ChatType(str, Enum):
    public = "public"
    private = "private"
    group = "group"


chat_database = [
    {
        "id": 1,
        "name": "Чат 1",
        "created_date": datetime(2022, 4, 20, 19, 39, 0),
        "type": ChatType.group,
        "messages_ids": [],
    }
]

user_chat_database = [
    {
        "user_id": 1,
        "chat_id": 1
    },
    {
        "user_id": 2,
        "chat_id": 1
    },
]


def create_chat(db: Session, chat: schema.Chat):
    """Создать чат"""
    chat_db = Chat(name=chat.name, type=chat.type, created_date=datetime.now())
    print(chat_db, "here1")
    db.add(chat_db)
    db.commit()

    return chat_db


def delete_chat(db: Session, chat_id: int):
    """Удалить чат"""
    db.query(Chat).filter(Chat.id == chat_id).delete()
    db.commit()


def get_chat_by_id(db: Session, chat_id: int):
    """Получить пользователя по id"""
    return db.query(Chat).filter(Chat.id == chat_id).one_or_none()


def get_user_by_chat_name(db: Session, chat_name: str):
    """Получить пользователя по логину"""
    return db.query(Chat).filter(Chat.login == chat_name).one_or_none()


def update_chat(db: Session, chat: schema.ChatInDB):
    """Обновить данные чата"""
    chat_db = db.query(Chat).filter(Chat.id == chat.id).one_or_none()
    for param, value in chat.dict().items():
        setattr(chat_db, param, value)
    db.commit()

    return chat_db