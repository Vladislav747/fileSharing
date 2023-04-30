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
    if count is not None and int(count) > 5:
        return HTTPException(status_code=422, detail="too much counts")

    initial_count = 0
    response.set_cookie(key="count", value=str(initial_count), max_age=60 * 60 * 24)
    file_name, link_to_download = await create_file(file=file, request=request)
    print(count, "dfss")

    return {"msg": f'{file_name} File loaded', "link_to_download": link_to_download}


@router.delete("/", status_code=status.HTTP_200_OK)
async def delete_file(file_name: str):
    return await delete_image(file_name=file_name)
