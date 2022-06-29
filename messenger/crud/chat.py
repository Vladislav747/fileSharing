from datetime import datetime
from enum import Enum
import schemas.chat as schema
from core.db.models import Chat, ChatMessage, Message
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

#Список из N последних сообщений в чате
def get_last_messages(db: Session, chat_id: int, number_of_messages: int):
    """Получить последние сообщения"""
    chats_db = db.query(ChatMessage.message_id, Message.message).filter(ChatMessage.chat_id == chat_id).join(Message, Message.id == ChatMessage.message_id).order_by(Message.id.desc()).limit(number_of_messages).all()
    return chats_db

def update_last_time_chat(db: Session, chat_id: int):
    """Обновить данные чата"""
    chat_db = db.query(Chat).filter(Chat.id == chat_id).one_or_none()
    setattr(chat_db, "last_message", datetime.now())
    db.commit()

    return chat_db

def get_last_chats(db: Session, number_of_chats: int):
    """Получить последние чаты по актуальности"""
    chats_db = db.query(Chat).order_by(Chat.last_message.desc()).limit(number_of_chats).all()
    return chats_db