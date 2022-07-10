from sqlalchemy.orm import Session
from core.db.models import UserChat


def create_link(db: Session, chat_id: int, user_id: int):
    """Создать связь"""
    # Проверяем что такой связи уже не существует
    if db.query(UserChat.id).filter_by(chat_id=chat_id, user_id=user_id).first() is None:
        chat_user_db = UserChat(chat_id=chat_id, user_id=user_id)
        db.merge(chat_user_db)
        db.commit()

        return chat_user_db
    else:
        return None

def get_all_users_in_chat(db: Session, chat_id: int):
    """Получить все id пользователей в чате"""
    users_in_chat = db.query(UserChat.user_id).filter(UserChat.chat_id == chat_id).all()

    db.commit()

    return users_in_chat
