from pydantic import BaseModel


class User(BaseModel):
    login: str
    password: str
    name: str


class UserInDb(User):
    id: int

    class Config:
        orm_mode = True
