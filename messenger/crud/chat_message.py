from sqlalchemy.orm import Session
from core.db.models import ChatMessage


def create_link(db: Session, chat_id: int, message_id: int):
    """Создать связь"""
    chat_message_db = ChatMessage(chat_id=chat_id, message_id=message_id)
    db.add(chat_message_db)
    db.commit()

    return chat_message_db
