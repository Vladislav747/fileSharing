from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from crud.user import authenticate
from deps import get_db
from security import create_access_token, create_refresh_token, refresh_token
from schemas.user import RefreshToken

router = APIRouter(prefix="/login")


@router.post("/")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db=Depends(get_db),
):
    user = authenticate(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неправильный логин или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(user_id=user.id)
    refresh_token = create_refresh_token(login=form_data.username)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/refresh-token")
def update_refresh_token(
    token: RefreshToken,
):
    """Обновить токен"""
    print(token.refresh_token, "token")
    new_tokens = refresh_token(token.refresh_token)
    return new_tokens