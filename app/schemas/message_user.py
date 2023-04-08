from pydantic import BaseModel


class MessageUser(BaseModel):
    message_id: int
    user_id: int
