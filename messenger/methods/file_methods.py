import os
from settings import *
from uuid import uuid4
import aiofiles
from fastapi import HTTPException, UploadFile


def get_file_size(filename, path : str = None):
    file_path = f'{UPLOADED_FILES_PATH}{filename}'
    if path:
        file_path = f'{path}{filename}'
    return os.path.getsize(file_path)


def delete_file_from_uploads(file_name):
    try:
        os.remove(UPLOADED_FILES_PATH + file_name)
    except Exception as e:
        print(e, "Error delete file")


async def save_video(
    file: UploadFile,
):
    file_name = f'{uuid4()}.png'
    # TODO Проверить формат разрешения
    if (file is not None):
        await save_file(file_name, file)
    else:
        raise HTTPException(status_code=418, detail="It isn't mp4")


async def save_file(file_name: str, file: UploadFile):
    file_path = f'{UPLOADED_FILES_PATH}{file_name}'
    async with aiofiles.open(file_path, "wb") as buffer:
        data = await file.read()
        # Пишу на жесткий диск
        await buffer.write(data)