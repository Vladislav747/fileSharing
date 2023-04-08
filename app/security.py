from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status

from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = "09d25e094faa6ca2556c818166bua9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """ Сгенерировать Хэш пароля

    Args:
        password: пароль
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    """ Верифицировать хэшированный пароль и обычный пароль

     Args:
        plain_password: пароль
        hashed_password: хэшированный пароль
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_id: int, expires_delta: Optional[timedelta] = None):
    """Сгенерировать access token"""
    to_encode = {"sub": str(user_id)}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_user_from_jwt(token: str):
    try:
        # Автоматически проверяет что если время токена вышло он выкидывает ошибку JWTError
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
    except JWTError:
        print("JWTError")
        return None

    return user_id


def create_refresh_token(login):
    """Сгенерировать refresh token"""
    expire = datetime.utcnow() + timedelta(
        minutes=REFRESH_TOKEN_EXPIRE_MINUTES
    )
    to_encode = {"exp": expire, "sub": str(login)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def refresh_token(refresh_token):
    """Обновить Referesh токен"""
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        new_access_token = create_access_token(payload["sub"])
        new_refresh_token = create_refresh_token(payload["sub"])
        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
        }
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
