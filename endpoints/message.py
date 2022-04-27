from fastapi import APIRouter
from schemas.message import Message

router = APIRouter(
    prefix="/messages",
    tags=['Messages']
)

messages_database = [
    {
        "id": 1,
        "user_id": 1,
        "chat_id": 1,
        "message": "Hello",
    },
    {
        "id": 2,
        "user_id": 2,
        "chat_id": 1,
        "message": "Hello to you",
    }
]


@router.get("/")
async def root():
    return messages_database

@router.get("/{message_id}")
async def get_message(message_id: int):
    return {"message": messages_database[message_id - 1]}


@router.post("/", response_model=Message)
async def add_message(message: Message):
    message_db = Message(id=len(messages_database) + 1, **message.dict())

    return message_db


@router.put("/{message_id}", response_model=Message)
async def update_message(message_id: int, message: Message):
    message_db = messages_database[message_id - 1]
    for param, value in message.dict().items():
        message_db[param] = value
    return message_db

@router.delete("/{message_id}", response_model=Message)
async def del_message(message_id: int):
    del messages_database[message_id]
