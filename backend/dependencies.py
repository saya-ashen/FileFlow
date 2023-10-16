from typing import Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .db.crud import get_user
from .db.database import SessionLocal
from .db.schemas import User
from .settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.TOKEN_URL)


class Token(BaseModel):
    access_token: str
    refresh_token: str
    expires: str


class LoginData(Token):
    username: str
    roles: list


class LoginResponse(BaseModel):
    success: bool
    data: LoginData
    access_token: str  # 为了兼容docs工具，这里返回的是access_token TODO: 以后删除


class TokenData(BaseModel):
    # username: Union[str, None] = None
    id: Union[int, None] = None


# 登录成功后返回的response


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        print(payload.get("sub"))
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(id=user_id)
    except JWTError as e:
        raise credentials_exception
    user = get_user(db, user_id=token_data.id)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
