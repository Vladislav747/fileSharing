from fastapi import APIRouter, status, UploadFile, Request
from fastapi.responses import FileResponse
from methods.file_methods import create_file, delete_image, get_file

router = APIRouter(
    prefix="/converter",
    tags=['converter']
)


@router.get("/download")
async def download_file(filename: str):
    file_path = await get_file(filename=filename)
    await delete_image(file_name=filename)
    return FileResponse(file_path)



@router.post("/", status_code=status.HTTP_200_OK)
async def send_file(file: UploadFile, request: Request):
    file_name, link_to_download = await create_file(file=file, request=request)

    return {"msg": f'{file_name} File loaded', "link_to_download": link_to_download}


@router.delete("/", status_code=status.HTTP_200_OK)
async def delete_file(file_name: str):
    return await delete_image(file_name=file_name)
