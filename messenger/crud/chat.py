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
    chat_db = Chat(name=chat.name, type=chat.type, created_date=datetime.now())
    print(chat_db, "here1")
    db.add(chat_db)
    db.commit()

    return chat_db
