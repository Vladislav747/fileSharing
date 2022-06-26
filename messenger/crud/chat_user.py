from sqlalchemy.orm import Session
from core.db.models import UserChat


def create_link(db: Session, chat_id: int, user_id: int):
    """Создать связь"""
    chat_user_db = UserChat(chat_id=chat_id, user_id=user_id)
    db.add(chat_user_db)
    db.commit()

    return chat_user_db
