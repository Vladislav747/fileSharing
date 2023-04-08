from fastapi import FastAPI
import uvicorn

from endpoints.converter import router as converter_router
from endpoints.user import router as user_router

app = FastAPI()

app.include_router(converter_router, tags=["converter"])
app.include_router(user_router, tags=["user"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host='0.0.0.0',
        port=8080,
        reload=True,
        debug=True,
    )