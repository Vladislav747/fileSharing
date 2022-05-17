from fastapi import APIRouter, Depends, HTTPException, status

from deps import get_db
import crud.user
from schemas.user import User, UserInDb

router = APIRouter(
    prefix="/user",
    tags=['Users']
)


@router.get("/")
async def get_users():
    return {"users": []}

@router.get("/{user_id}")
async def get_user(user_id: int, db=Depends(get_db)):
    """Получить пользователя по заданному user_id"""
    user = crud.user.get_user_by_id(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return user


@router.post("/", response_model=UserInDb)
async def create_user(user: User, db=Depends(get_db)):
    """Создать пользователя"""
    result = crud.user.create_user(db=db, user=user)
    return result


@router.put("/{user_id}", response_model=UserInDb)
async def update_user(user_id: int, user: User, db=Depends(get_db)):
    """Изменить пользователя"""
    user_db = crud.user.update_user(db=db, user_id=user_id, user=user)

    return user_db


@router.delete("/{user_id}")
async def delete_user(user_id: int, db=Depends(get_db)):
    """Удалить пользователя"""
    crud.user.delete_user(db=db, user_id=user_id)