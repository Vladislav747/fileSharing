from fastapi import APIRouter, HTTPException, Depends, status
from schemas.message import Message, MessageInDB
import crud.message as crud
import crud.message_user as crud_message_user
import crud.chat_message as crud_chat_message
import crud.chat_user as crud_chat_user
import crud.chat as crud_chat
from deps import get_db

router = APIRouter(
    prefix="/messages",
    tags=['Messages']
)


@router.get("/")
async def get_all_messages(db=Depends(get_db)):
    return crud.get_all_messages(db)


@router.get("/{message_id}")
async def get_message(message_id: int, db=Depends(get_db)):
    return crud.get_message_by_id(db, message_id)


@router.post("/", response_model=MessageInDB)
async def add_message(message: Message, db=Depends(get_db)):
    result = crud.create_message(db, message)
    # Добавить связку в таблицу MessageUser между пользователем и сообщением
    result_message_user = crud_message_user.create_link(db, message_id=result.id, user_id=message.user_id)
    # Добавить связку в таблицу MessageChat между чатом и сообщением
    result_chat_message = crud_chat_message.create_link(db, chat_id=message.chat_id, message_id=result.id)
    # Добавить связку в таблицу UserChat между чатом и сообщением
    result_chat_message = crud_chat_user.create_link(db, chat_id=message.chat_id, user_id=message.user_id)
    # Добавить обновление для last_message для  чата
    result_chat_message = crud_chat.update_last_time_chat(db, chat_id=message.chat_id)
    return result


@router.put("/", response_model=MessageInDB)
async def update_message(message: MessageInDB, db=Depends(get_db)):
    # Редактирование сообщения подразумевает только изменение текста
    message_db = crud.update_chat(db=db, message=message)
    return message_db


@router.delete("/{message_id}", status_code=200)
async def del_message(message_id: int, db=Depends(get_db)):
    # Проверяем что у нас есть такое сообщен ие
    message = crud.get_message_by_id(db=db, message_id=message_id)
    if message is not None:
        crud.delete_message(db=db, message_id=message_id)
        return "Сообщение успешно удалено"
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Не найден id сообщение",
        )
