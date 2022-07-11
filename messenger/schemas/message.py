import datetime

from pydantic import BaseModel

from typing import Optional


class Message(BaseModel):
    message: str
    chat_id: int
    delayed: Optional[bool]
    timeoutInS: Optional[int]


class MessageEdit(BaseModel):
    id: int
    message: str
    user_id: int


class MessageInDB(BaseModel):
    id: int
    message: str
    created_date: Optional[datetime.datetime]
    updated_date: Optional[datetime.datetime]

    class Config:
        orm_mode = True


class MessageRead(BaseModel):
    chat_id: int
