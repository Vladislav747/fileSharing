from fastapi import APIRouter, Depends, Response, Cookie

from schemas.user import User, UserInDB, UserCreate
from deps import get_db, get_current_user
import crud.user as crud

router = APIRouter(prefix="/user")


@router.get("/increase_count")
async def increase_count(response: Response, count: str | None = Cookie(default=None),
                         name: str | None = Cookie(default=None)):
    new_count = int(count) + 1
    response.set_cookie(key="count", value=new_count)

    return {"count": new_count, "name": name}


@router.post("/delete_session")
async def del_session(response: Response):
    response.delete_cookie(key="count")
    return "deleted session"


@router.post("/", response_model=UserInDB)
async def create_user(user: UserCreate, db=Depends(get_db)):
    """Создать пользователя"""
    result = crud.create_user(db=db, user=user)
    return result
