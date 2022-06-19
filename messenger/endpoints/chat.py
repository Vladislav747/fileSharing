from fastapi import APIRouter
from schemas.chat import Chat
from crud.chat import chat_database

router = APIRouter(
    prefix="/chat",
    tags=['Chats']
)


@router.get("/")
async def root():
    return chat_database


@router.get("/{chat_id}")
async def get_chat(chat_id: int):
    return {"chat": chat_database[chat_id - 1]}


# Список из N последних сообщений в чате
@router.get("/last/{chat_id}/{number_of_messages}")
async def get_last_messages(number_of_messages: int):
    return chat_database[0]["messages_ids"][-number_of_messages:]


@router.post("/", response_model=Chat)
async def add_chat(chat: Chat):
    chat_db = Chat(id=len(chat_database) + 1, **chat.dict())

    return chat_db


@router.put("/{user_id}", response_model=Chat)
async def update_chat(chat_id: int, user: Chat):
    user_db = chat_database[chat_id - 1]
    for param, value in user.dict().items():
        user_db[param] = value
    return user_db


@router.delete("/{user_id}", response_model=Chat)
async def del_chat(chat_id: int):
    del chat_database[chat_id]