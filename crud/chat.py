from datetime import datetime

from enum import Enum

class ChatType (str, Enum):
    public = "public"
    private = "private"
    group = "group"

chat_db = [
    {
        "id": 1,
        "name": "Чат 1",
        "created_date": datetime(2022, 4, 20, 19, 39, 0),
        "type" : "ad"
    }
]