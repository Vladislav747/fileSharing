from fastapi import APIRouter, status, UploadFile, HTTPException, Request
from fastapi.responses import FileResponse
from methods.file_methods import create_file, delete_image
import os
from settings import *

router = APIRouter(
    prefix="/converter",
    tags=['converter']
)


@router.get("/download")
async def download_file(filename: str, request: Request):
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

    host = request.headers["host"]
    print(host, "host")
    return FileResponse(file_path)


@router.post("/", status_code=status.HTTP_200_OK)
async def send_file(file: UploadFile):
    file_name = await create_file(file=file)

    return f'{file_name} File loaded'


@router.delete("/", status_code=status.HTTP_200_OK)
async def delete_file(file_name: str):
    return await delete_image(file_name=file_name)
