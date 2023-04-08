import os
from settings import *
from uuid import uuid4
import aiofiles
from fastapi import HTTPException, UploadFile, File
from PIL import Image


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


async def create_file(
    file: UploadFile,
):
    file_name = f'{uuid4()}.png'
    # TODO Проверить формат разрешения
    if (file is not None):
        file_is_png = await check_file_is_image(file)
        if(file_is_png is True):
            await save_file(file_name=file_name, file=file)
        else:
            raise HTTPException(status_code=400, detail="File is not png or is not image")
    else:
        raise HTTPException(status_code=418, detail="It isn't mp4")


async def save_file(file_name: str, file: UploadFile):
    file_path = f'{UPLOADED_FILES_PATH}{file_name}'
    async with aiofiles.open(file_path, "wb") as buffer:
        data = await file.read()
        # Пишу на жесткий диск
        await buffer.write(data)

async def convert_image(file: UploadFile = File(...)):
    image = Image.open(file.file)
    if image.format != "PNG":
        return {"error": "File is not in PNG format"}

    # Convert PNG to JPEG
    image = image.convert("RGB")
    new_file_name = file.filename.replace(".png", ".jpeg")
    image.save(new_file_name, "JPEG")

    return {"file_name": new_file_name}


async def check_file_is_image(file: UploadFile = File(...)):
    # Attempt to open file as image
    try:
        image = Image.open(file.file)
        if image.format != "PNG":
            return {"error": "File is not in PNG format"}
    except:
        return {"error": "File is not an image"}

    return True


async def delete_image(file_name: str):
    # specify the folder where the files are located
    folder = UPLOADED_FILES_PATH
    # get the file path by joining the folder path and file name
    file_path = os.path.join(folder, file_name)
    # check if the file exists
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    # delete the file
    os.remove(file_path)
    return {"message": "File deleted"}