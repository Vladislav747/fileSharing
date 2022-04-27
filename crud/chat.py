from datetime import datetime
from schemas.chat import ChatType

chat_db = [
    {
        "id": 1,
        "name": "Чат 1",
        "created_date": datetime(2022, 4, 20, 19, 39, 0),
        "type" : ChatType.public,
    }
]