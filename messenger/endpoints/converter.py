from fastapi import APIRouter, status, UploadFile, HTTPException
from fastapi.responses import FileResponse
from methods.file_methods import save_video
import os
from settings import *

router = APIRouter(
    prefix="/converter",
    tags=['converter']
)


@router.get("/download")
async def download_file(filename: str):
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
    return FileResponse(file_path)


@router.post("/", status_code=status.HTTP_200_OK)
async def send_file(file: UploadFile):
    await save_video(file)

    return "File loaded"


@router.delete("/", status_code=status.HTTP_200_OK)
async def delete_file(file_name: str):
    print(file_name, "file_name delete")
    # await delete_img(file_name)

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
