import os
from settings import *
from uuid import uuid4
import aiofiles.os
from fastapi import HTTPException, UploadFile, File, Request
from PIL import Image
from typing import NamedTuple

class CreateFileResponse(NamedTuple):
    file_name: str
    link: str


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
    request: Request
):
    file_name = f'{uuid4()}.jpeg'
    # TODO Проверить формат разрешения
    if (file is not None):
        new_file_name = await convert_image(file_name=file_name, file=file)
        # host = request.headers["host"]
        link_to_download = f'localhost:8080/converter/download?filename={new_file_name}'
        return CreateFileResponse(file_name, link_to_download)
    else:
        raise HTTPException(status_code=418, detail="It isn't mp4")

async def convert_image(file_name: str, file: UploadFile = File(...)):
    # Convert PNG to JPEG 
    with Image.open(file.file) as im:
        if im.format != "PNG":
            raise HTTPException(status_code=422, detail="Wrong file format")
        im.convert('RGB').save(
            f'{UPLOADED_FILES_PATH}{file_name}'
        ) 

    return file_name


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
    if not await aiofiles.os.path.isfile(f'{UPLOADED_FILES_PATH}{file_name}'):
        raise HTTPException(status_code=404, detail="File not found")
    # delete the file
    await aiofiles.os.remove(f'{UPLOADED_FILES_PATH}{file_name}')
    return {"message": "File deleted"}


async def get_file(filename: str):
    # specify the folder where the files are located
    folder = UPLOADED_FILES_PATH
    # get the file path by joining the folder path and file name
    file_path = folder + "/" + filename
    # check if the file exists
    try:
        file = open(file_path, "rb")
        file.close()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    # return the file as a response using the FileResponse class

    return file_path