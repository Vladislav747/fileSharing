from pydantic import BaseModel


class ChatUser(BaseModel):
    chat_id: int
    user_id: int
