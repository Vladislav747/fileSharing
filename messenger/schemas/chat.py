from pydantic import BaseModel
from typing import List
from datetime import datetime

from enum import Enum


class ChatType(str, Enum):
    public = "public"
    private = "private"
    group = "group"


class Chat(BaseModel):
    name: str
    type: ChatType


class ChatInDB(Chat):
    id: int

    class Config:
        orm_mode = True