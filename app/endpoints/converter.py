from fastapi import APIRouter, status, UploadFile, Request, Cookie, HTTPException, Response
from fastapi.websockets import WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from redis import Redis
from methods.file_methods import create_file, delete_image, get_file
from worker import create_task

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
    # celery задание
    create_task.delay()
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


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    print("here")

    while True:
        try:
            # Receive message from the frontend
            message = await websocket.receive_text()

            # Publish the message to Redis
            Redis.publish("channel", message)

        except WebSocketDisconnect:
            break


# Subscriber coroutine
async def subscribe(websocket):
    pubsub = Redis.pubsub()
    pubsub.subscribe("channel")

    # Read messages from Redis and send them to the subscribed websocket
    for message in pubsub.listen():
        if message["type"] == "message":
            data = message["data"].decode("utf-8")
            await websocket.send_text(data)
