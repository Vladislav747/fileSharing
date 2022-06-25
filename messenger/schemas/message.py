import datetime

from pydantic import BaseModel


class Message(BaseModel):
    message: str
    user_id: int
    chat_id: int


class MessageInDB(BaseModel):
    id: int
    message: str
    created_date: datetime.datetime

    class Config:
        orm_mode = True
