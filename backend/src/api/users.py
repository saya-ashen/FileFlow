from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..db.crud import create_user, get_user_by_email, get_user_by_username
from ..db.schemas import User, UserCreate
from ..dependencies import (
    LoginData,
    LoginResponse,
    RefreshResponse,
    RefreshToken,
    Token,
    get_current_active_user,
    get_db,
)
from ..utils import (
    create_access_token,
    create_refresh_token,
    verify_password,
    verify_refresh_token,
)

router = APIRouter(prefix="/api")


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


@router.post("/login", response_model=LoginResponse)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(
        db, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token, expires_access = create_access_token(user.id)
    refresh_token, expire_refresh = create_refresh_token(user.id)
    response = LoginResponse(
        success=True,
        data=LoginData(
            username=user.username,
            roles=["admin"],
            access_Token=access_token,
            refresh_Token=refresh_token,
            expires=expires_access,  # TODO
        ),
        access_token=access_token,
    )
    return response


@router.post("/refreshToken", response_model=RefreshResponse)
async def refresh_token(refresh_token: RefreshToken):
    payload = verify_refresh_token(refresh_token.refresh_Token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token, expires = create_access_token(payload.get("sub"))
    reponse = RefreshResponse(
        success=True,
        data=Token(
            access_Token=access_token,
            refresh_Token=refresh_token.refresh_Token,
            expires=expires,
        ),
    )
    return reponse


@router.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


# 注册用户
@router.post("/register")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="邮箱已存在")
    user = create_user(db=db, user=user)
    access_token, expires_access = create_access_token(user.id)
    refresh_token, expire_refresh = create_refresh_token(user.id)
    response = LoginResponse(
        success=True,
        data=LoginData(
            username=user.username,
            roles=["admin"],
            access_Token=access_token,
            refresh_Token=refresh_token,
            expires=expires_access,  # TODO
        ),
        access_token=access_token,
    )
    return response


@router.get("/getAsyncRoutes")
async def get_async_routes():
    router = {
        "path": "/file",
        "meta": {"title": "其他", "icon": "folder", "rank": 10},
    }

    return {"success": True, "data": [router]}
