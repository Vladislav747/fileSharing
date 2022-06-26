from fastapi import APIRouter, HTTPException, Depends, status
from schemas.message import Message, MessageInDB
import crud.message as crud
import crud.message_user as crud_message_user
import crud.chat_message as crud_chat_message
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
    result_message_user = crud_message_user.create_link(db, message)
    # Добавить связку в таблицу ChatUser между чатом и сообщением
    result_chat_message = crud_chat_message.create_link(db, message)
    return result
    # message_db = Message(id=len(messages_database) + 1, **message.dict()).dict()
    # # Метка что чат найден
    # found_chat = False
    # # Поместить id сообщения к чату
    # for chat in chat_database:
    #     if chat["id"] == message_db["chat_id"]:
    #         chat["messages_ids"].append(len(messages_database) + 1)
    #         found_chat = True
    # # Если чат к которому нужно подцепить сообщение не найден кидаем ошибку
    # if found_chat == True:
    #     return message_db
    # else:
    #     raise HTTPException(status_code=422, detail="Chat not found")


@router.put("/{message_id}", response_model=Message)
async def update_message(message_id: int, message: Message):
    # Редактирование сообщения подразумевает только изменение текста
    message_db = crud.messages_database[message_id - 1]
    for param, value in message.dict().items():
        message_db[param] = value
    return message_db


@router.delete("/{message_id}", status_code=200)
async def del_message(message_id: int, db=Depends(get_db)):
    # Проверяем что у нас есть такое сообщение
    message = crud.get_message_by_id(db=db, message_id=message_id)
    if message is not None:
        crud.delete_message(db=db, message_id=message_id)
        return "Сообщение успешно удалено"
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Не найден id сообщение",
        )

    #     # Метка что сообщение найдено
#     found_message = False
#
#     del messages_database[message_id - 1]
#     # Пробежаться по всем чатам
#     # и посмотреть где содержится id сообщения и удалить из списка
#     for chat in chat_database:
#         if message_id in chat["messages_ids"]:
#             index = chat["messages_ids"].index(message_id)
#             del chat["messages_ids"][index]
#
#     return chat_database
