from fastapi import APIRouter, status, UploadFile, Request, Cookie, HTTPException, Response
from fastapi.responses import FileResponse
from methods.file_methods import create_file, delete_image, get_file

from starlette.background import BackgroundTasks

router = APIRouter(
    prefix="/converter",
    tags=['converter']
)


@router.get("/download")
async def download_file(filename: str, background_tasks: BackgroundTasks):
    file_path = await get_file(filename=filename)
    background_tasks.add_task(delete_image, file_name=filename)
    return FileResponse(file_path)


@router.post("/", status_code=status.HTTP_200_OK)
async def send_file(file: UploadFile, request: Request, response: Response, count: str | None = Cookie(default=None)):
    # Валидируем что файл загружается только формата image/png
    if file.content_type != "image/png":
        return HTTPException(status_code=422, detail="only png files are allowed")

    if count is not None and int(count) > 5:
        return HTTPException(status_code=422, detail="too much counts")

    initial_count = 0
    response.set_cookie(key="count", value=str(initial_count), max_age=60 * 60 * 24)
    print(file.content_type, "file.content_type")
    file_name, link_to_download = await create_file(file=file, request=request)

    return {"msg": f'{file_name} File loaded', "link_to_download": link_to_download}


@router.delete("/", status_code=status.HTTP_200_OK)
async def delete_file(file_name: str):
    return await delete_image(file_name=file_name)
