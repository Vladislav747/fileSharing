from pydantic import BaseModel
from typing import List

from enum import Enum


class ChatType(str, Enum):
    public = "public"
    private = "private"
    group = "group"


class Chat(BaseModel):
    id: int
    name: str
    users_ids: int
    type: ChatType
    messages_ids: List[int]
