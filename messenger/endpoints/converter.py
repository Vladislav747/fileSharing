import aiofiles
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from uuid import uuid4

router = APIRouter(
    prefix="/converter",
    tags=['converter']
)


@router.get("/")
async def root():
    return "hello"


@router.post("/")
async def send_file(file: UploadFile):
    await save_video(file)

    return "hello"


async def save_video(
        file: UploadFile,
):
    file_name = f'{uuid4()}.png'
    # TODO Проверить формат разрешения
    if (file is not None):
        await write_video(file_name, file)
    else:
        raise HTTPException(status_code=418, detail="It isn't mp4")


async def write_video(file_name: str, file: UploadFile):
    async with aiofiles.open(file_name, "wb") as buffer:
        data = await file.read()
        # Пишу на жесткий диск
        await buffer.write(data)
