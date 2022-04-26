from pydantic import BaseModel

class Message(BaseModel):
    message: str
    user_id: str


class MessageInDb(Message):
    id: int
