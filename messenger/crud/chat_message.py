from sqlalchemy.orm import Session
from core.db.models import ChatMessage


def create_link(db: Session, chat_id: int, message_id: int):
    """Создать связь"""
    # Проверяем что такой связи уже не существует
    if db.query(ChatMessage.id).filter_by(chat_id=chat_id, message_id=message_id).first() is None:
        chat_message_db = ChatMessage(chat_id=chat_id, message_id=message_id)
        db.add(chat_message_db)
        db.commit()

        return chat_message_db

    else:
        return None