from fastapi import FastAPI
import uvicorn

from endpoints.user import router as user_router
from endpoints.message import router as message_router
from endpoints.chat import router as chat_router

from core.db.models import Base
from core.db.session import engine

app = FastAPI()

app.include_router(user_router)
app.include_router(chat_router)
app.include_router(message_router)

if __name__=="__main__":
    Base.metadata.create_all(engine)
    uvicorn.run(
        "main:app",
        host='0.0.0.0',
        port=8080,
        reload=True,
        debug=True,
    )