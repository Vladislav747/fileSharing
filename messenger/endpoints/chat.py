from fastapi import APIRouter, Depends, HTTPException, status
from schemas.chat import Chat, ChatInDB
from deps import get_db, get_current_user
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


@router.get("/last-messages/")
async def get_last_messages(number_of_messages: int, chat_id: int, db=Depends(get_db)):
    """Список из N последних сообщений в чате"""
    chat_db = crud.get_last_messages(db=db, chat_id=chat_id, number_of_messages=number_of_messages)

    return chat_db

@router.get("/last-chats/")
async def get_last_chats(number_of_chats: int, db=Depends(get_db)):
    """Список из N последних чатов где были сообщения"""
    chat_db = crud.get_last_chats(db=db, number_of_chats=number_of_chats)

    return chat_db


@router.post("/", response_model=ChatInDB)
async def add_chat(chat: Chat, db=Depends(get_db), user_id=Depends(get_current_user)):
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not Authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
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

    if chat is not None:
        crud.delete_chat(db=db, chat_id=chat_id)
        return "Чат успешно удален"
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Не найден id чата",
        )
