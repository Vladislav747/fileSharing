from fastapi import APIRouter, HTTPException, Depends, status
from schemas.message import Message, MessageInDB, MessageEdit, MessageRead
import requests

import crud.message as crud
import crud.message_user as crud_message_user
import crud.message_user_readed as crud_message_user_readed
import crud.user as crud_user

from deps import get_db, get_current_user

from core.broker.celery import celery_app

router = APIRouter(
    prefix="/messages",
    tags=['Messages']
)

@router.get("/get-tags/{message_id}", status_code=200)
async def get_all_tags_messages(message_id: int, db=Depends(get_db)):
    """Получить все хэштеги из сообщения"""
    # Проверяем что у нас есть такое сообщение
    message = crud.get_message_by_id(db=db, message_id=message_id)
    if message is not None:
        parsed_msg = await requests.post("http://localhost:8080/extra-tags", message.message)
        return parsed_msg
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Не найдено сообщение",
        )

@router.get("/")
async def get_all_messages(db=Depends(get_db)):
    return crud.get_all_messages(db)

@router.get("/readed", status_code=200)
async def get_all_readed_messages(chat_id: int, db=Depends(get_db), user_id=Depends(get_current_user)):
    # Проверяем что у нас есть такой пользователь
    user = crud_user.get_user_by_id(db=db, user_id=user_id)
    if user is not None:
        messages_readed = crud_message_user_readed.get_all_readed_messages_in_chat(db=db, user_id=user_id, chat_id=chat_id)
        return messages_readed
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Не найден пользователь",
        )




@router.get("/{message_id}")
async def get_message(message_id: int, db=Depends(get_db)):
    return crud.get_message_by_id(db, message_id)


@router.post("/read-messages", status_code=200)
async def update_message_user_read(read_body: MessageRead, db=Depends(get_db), user_id=Depends(get_current_user)):
    result = crud_message_user_readed.update_message_user_read(db, chat_id=read_body.chat_id, user_id=user_id)
    return result



@router.post("/", status_code=200)
async def add_message(message: Message, db=Depends(get_db), user_id=Depends(get_current_user)):
    print(message.delayed, "delayed")
    if message.delayed is True:
        print("here")
        celery_app.send_task("queue.message", message=message, timeout=message.timeoutInS)
    else:
        result = await crud.create_message(db, message, user_id)

    return {"msg": "Сообщение успешно создано"}


@router.put("/", response_model=MessageInDB)
async def update_message(message: MessageInDB, db=Depends(get_db), user_id=Depends(get_current_user)):
    current_msg = crud_message_user.get_message_by_id(db=db, message_id=message.id)
    # Позволить менять сообщение только если пользователь являяется его автором
    if int(current_msg.user_id) == int(user_id):
        # Редактирование сообщения подразумевает только изменение текста
        message_db = crud.update_message(db=db, message=message)
        print(message_db.updated_date, "upd")
        return message_db
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Вы не можете редактировать сообщение",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.delete("/{message_id}", status_code=200)
async def del_message(message_id: int, db=Depends(get_db)):
    # Проверяем что у нас есть такое сообщение
    message = crud.get_message_by_id(db=db, message_id=message_id)
    if message is not None:
        current_msg = crud_message_user.get_message_by_id(db=db, message_id=message.id)
        # Позволить менять сообщение только если пользователь являяется его автором
        crud.delete_message(db=db, message_id=message_id)
        return "Сообщение успешно удалено"
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Не найден id сообщение",
        )
