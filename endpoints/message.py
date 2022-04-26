from fastapi import APIRouter
from schemas.message import Message, MessageInDb

router = APIRouter(
    prefix="/message",
    tags=['Messages']
)


@router.get("/")
async def root():
    return {"detail": "Not Found"}

messages_database = [
    {
        "id": 1,
        "user_id": "1",
        "message": "Hello",
    },
    {
        "id": 2,
        "user_id": "2",
        "message": "Hello to you",
    }
]

@router.get("/{message_id}")
async def get_message(message_id: int):
    return {"user": messages_database[message_id - 1]}


@router.post("/", response_model=MessageInDb)
async def add_message(message: Message):
    message_db = MessageInDb(id=len(messages_database) + 1, **message.dict())

    return message_db


@router.put("/{message_id}", response_model=MessageInDb)
async def update_message(message_id: int, message: Message):
    user_db = messages_database[message_id - 1]
    for param, value in message.dict().items():
        user_db[param] = value
    return user_db

@router.delete("/{user_id}", response_model=MessageInDb)
async def del_user(message_id: int):
    del messages_database[message_id]
