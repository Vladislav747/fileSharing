from sqlalchemy.orm import Session
import schemas.user as schema
from security import get_password_hash, verify_password
from core.db.models import User


def create_user(db: Session, user: schema.UserCreate):
    """Создать пользователя"""
    hashed_password = get_password_hash(user.password)
    user_db = User(login=user.login, hashed_password=hashed_password)
    db.add(user_db)
    db.commit()

    return user_db


def get_user_by_login(db: Session, login: str):
    """Получить пользователя по логину"""
    return db.query(User).filter(User.login == login).one_or_none()


def authenticate(db: Session, login: str, password: str):
    """Авторизация пользователя"""
    user = get_user_by_login(db, login)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
