from fastapi import FastAPI

from endpoints.user import router as user_router
from schemas.user import User, UserInDb

app = FastAPI()

app.include_router(user_router, prefix='/user', tags=['user'])


@app.get("/")
async def root():
    return {"message": "Hello World"}


users_database = [
    {
        "id": 1,
        "login": "main",
        "password": "asd",
        "name": "asd"
    },
    {
        "id": 2,
        "login": "main",
        "password": "asd",
        "name": "asd"
    }
]


@app.get("/user/{user_id}")
async def get_user(user_id: int):
    return {"user": users_database[user_id - 1]}


@app.post("/user", response_model=UserInDb)
async def add_user(user: User):
    user_db = UserInDb(id=len(users_database) + 1, **user.dict())

    return user_db


@app.put("/user/{user_id}", response_model=UserInDb)
async def update_user(user_id: int, user: User):
    user_db = users_database[user_id - 1]
    for param, value in user.dict().items():
        user_db[param] = value
    return user_db

@app.delete("/user/{user_id}", response_model=UserInDb)
async def del_user(user_id: int):
    del users_database[user_id]
