from fastapi import APIRouter, HTTPException
from schemas.message import Message
from crud.message import messages_database
from crud.chat import chat_database

router = APIRouter(
    prefix="/messages",
    tags=['Messages']
)


@router.get("/")
async def root():
    return messages_database


@router.get("/{message_id}")
async def get_message(message_id: int):
    return {"message": messages_database[message_id - 1]}


@router.post("/", response_model=Message)
async def add_message(message: Message):
    message_db = Message(id=len(messages_database) + 1, **message.dict()).dict()
    # Метка что чат найден
    found_chat = False
    # Поместить id сообщения к чату
    for chat in chat_database:
        if chat["id"] == message_db["chat_id"]:
            chat["messages_ids"].append(len(messages_database) + 1)
            found_chat = True
    # Если чат к которому нужно подцепить сообщение не найден кидаем ошибку
    if found_chat == True:
        return message_db
    else:
        raise HTTPException(status_code=422, detail="Chat not found")


@router.put("/{message_id}", response_model=Message)
async def update_message(message_id: int, message: Message):
    # Редактирование сообщения подразумевает только изменение текста
    message_db = messages_database[message_id - 1]
    for param, value in message.dict().items():
        message_db[param] = value
    return message_db


@router.delete("/{message_id}")
async def del_message(message_id: int):
    del messages_database[message_id - 1]
    # Пробежаться по всем чатам
    # и посмотреть где содержится id сообщения и удалить из списка
    for chat in chat_database:
        if message_id in chat["messages_ids"]:
            index = chat["messages_ids"].index(message_id)
            del chat["messages_ids"][index]

    return chat_database
