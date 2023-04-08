from pydantic import BaseModel


class ChatMessage(BaseModel):
    chat_id: int
    message_id: int
