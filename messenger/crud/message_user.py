from sqlalchemy.orm import Session
from core.db.models import MessageUser


def create_link(db: Session, user_id: int, message_id: int):
    """Создать связь"""
    message_user_db = MessageUser(user_id=user_id, message_id=message_id)
    db.add(message_user_db)
    db.commit()

    return message_user_db