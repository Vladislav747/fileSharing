from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
        
    id  = Column(Integer, primary_key=True, index=True)
    login = Column(String)
    password = Column(String)
    name = Column(String(40))


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    created_data = Column(DateTime, server_default=func.now())

class UserChat(Base):
    __tablename__ = "users_chats"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    chat_id = Column(Integer, ForeignKey('chats.id'))

