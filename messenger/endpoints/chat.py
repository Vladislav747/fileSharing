from fastapi import APIRouter, Depends
from schemas.chat import Chat, ChatInDB
from deps import get_db
import crud.chat as crud

router = APIRouter(
    prefix="/chat",
    tags=['Chats']
)


@router.get("/")
async def root():
    return crud.chat_database


@router.get("/{chat_id}")
async def get_chat(chat_id: int):
    return {"chat": crud.chat_database[chat_id - 1]}


# Список из N последних сообщений в чате
@router.get("/last/{chat_id}/{number_of_messages}")
async def get_last_messages(number_of_messages: int):
    return crud.chat_database[0]["messages_ids"][-number_of_messages:]


@router.post("/", response_model=ChatInDB)
async def add_chat(chat: Chat, db=Depends(get_db)):
    result = crud.create_chat(db=db, chat=chat)
    print(result, "here")
    return result


@router.put("/{user_id}", response_model=Chat)
async def update_chat(chat_id: int, user: Chat):
    user_db = crud.chat_database[chat_id - 1]
    for param, value in user.dict().items():
        user_db[param] = value
    return user_db


@router.delete("/{user_id}", response_model=Chat)
async def del_chat(chat_id: int):
    del crud.chat_database[chat_id]
