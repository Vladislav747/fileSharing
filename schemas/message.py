from pydantic import BaseModel

class Message(BaseModel):
    id: int
    message: str
    user_id: int
    chat_id: int
