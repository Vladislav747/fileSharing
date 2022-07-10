from sqlalchemy.orm import Session
from core.db.models import MessageUser


def create_link(db: Session, user_id: int, message_id: int):
    """Создать связь"""
    # Проверяем что такой связи уже не существует
    if db.query(MessageUser.id).filter_by(user_id=user_id, message_id=message_id).first() is None:
        message_user_db = MessageUser(user_id=user_id, message_id=message_id)
        db.add(message_user_db)
        db.commit()

        return message_user_db
    else:
        return None


def get_message_by_id(db: Session, message_id: int):
    """Получить сообщение по id"""
    return db.query(MessageUser).filter(MessageUser.message_id == message_id).one_or_none()
