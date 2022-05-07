from fastapi import APIRouter
from schemas.chat import Chat
from crud.chat import chats_db

router = APIRouter(
    prefix="/chat",
    tags=['Chats']
)


@router.get("/")
async def root():
    return chats_db


@router.get("/{chat_id}")
async def get_chat(chat_id: int):
    return {"chat": chats_db[chat_id - 1]}


# Список из N последних сообщений в чате
@router.get("/last/{chat_id}/{number_of_messages}")
async def get_last_messages(number_of_messages: int):
    return chats_db[0]["messages_ids"][-number_of_messages:]


@router.post("/", response_model=Chat)
async def add_chat(chat: Chat):
    chat_db = Chat(id=len(chats_db) + 1, **chat.dict())

    return chat_db


@router.put("/{user_id}", response_model=Chat)
async def update_chat(chat_id: int, user: Chat):
    user_db = chats_db[chat_id - 1]
    for param, value in user.dict().items():
        user_db[param] = value
    return user_db


@router.delete("/{user_id}", response_model=Chat)
async def del_chat(chat_id: int):
    del chats_db[chat_id]
