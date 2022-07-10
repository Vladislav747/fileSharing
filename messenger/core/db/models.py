from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String)
    hashed_password = Column(String)
    name = Column(String)


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    created_date = Column(DateTime, server_default=func.now())
    type = Column(String)
    last_message = Column(DateTime, nullable=True)


class UserChat(Base):
    __tablename__ = "users_chats"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    chat_id = Column(Integer, ForeignKey('chats.id'))


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String)
    created_date = Column(DateTime, server_default=func.now())
    updated_date = Column(DateTime, server_default=func.now())
    changed = Column(Boolean)


class ChatMessage(Base):
    __tablename__ = "chats_messages"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey('chats.id'))
    message_id = Column(Integer, ForeignKey('messages.id'))


class MessageUser(Base):
    __tablename__ = "users_messages"

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey('messages.id'))
    user_id = Column(Integer, ForeignKey('users.id'))


class MessageUserRead(Base):
    __tablename__ = "messages_user_read"

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey('messages.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    message_is_read = Column(Boolean)
