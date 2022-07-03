from pydantic import BaseModel


class User(BaseModel):
    login: str
    name: str


class UserCreate(User):
    password: str


class UserInDB(User):
    id: int

    class Config:
        orm_mode = True


class RefreshToken(BaseModel):
    refresh_token: str
