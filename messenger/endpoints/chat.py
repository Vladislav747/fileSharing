from fastapi import APIRouter, Depends, HTTPException, status
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


@router.get("/{chat_id}", response_model=ChatInDB)
async def get_chat(chat_id: int, db=Depends(get_db)):
    """Получить чат по заданному chat_id"""
    chat = crud.get_chat_by_id(db=db, chat_id=chat_id)
    if chat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return chat


@router.get("/last/{chat_id}/{number_of_messages}")
async def get_last_messages(number_of_messages: int):
    """Список из N последних сообщений в чате"""
    return crud.chat_database[0]["messages_ids"][-number_of_messages:]


@router.post("/", response_model=ChatInDB)
async def add_chat(chat: Chat, db=Depends(get_db)):
    result = crud.create_chat(db=db, chat=chat)

    return result


@router.put("/", response_model=ChatInDB)
async def update_chat(chat: ChatInDB, db=Depends(get_db)):
    """Изменить чат"""
    chat_db = crud.update_chat(db=db, chat=chat)

    return chat_db


@router.delete("/{chat_id}", status_code=200)
async def del_chat(chat_id: int, db=Depends(get_db)):
    # Проверяем что у нас есть такой чат
    chat = crud.get_chat_by_id(db=db, chat_id=chat_id)
    print(chat, "chat")
    if chat is not None:
        crud.delete_chat(db=db, chat_id=chat_id)
        return "Чат успешно удален"
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Не найден id чата",
        )
