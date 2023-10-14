from typing import Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..settings import settings
from .db.crud import get_user
from .db.database import SessionLocal
from .db.schemas import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    # username: Union[str, None] = None
    id: Union[int, None] = None


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(token: str, db: Session):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
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


async def get_current_active_user(token: str, db: Session):
    current_user = await get_current_user(token=token, db=db)
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
