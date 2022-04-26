from fastapi import FastAPI

from endpoints.user import router as user_router

app = FastAPI()

app.include_router(user_router)
app.include_router(message_router)