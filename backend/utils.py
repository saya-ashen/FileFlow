import os
from datetime import datetime, timedelta
from typing import Any, Union

from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from .db import crud, models, schemas
from .settings import settings

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_REFRESH_SECRET_KEY, settings.ALGORITHM
    )
    return encoded_jwt


# 获取用户的根目录路径
def get_root_path(user: schemas.User) -> str:
    return f"{settings.ROOT_PATH}/UserStorage/{user.username}"


# 删除文件或文件夹
def delete(item_create: schemas.ItemCreate, user: schemas.User) -> bool:
    user_root_path = get_root_path(user)
    file_path = f"{user_root_path}/{item_create.path}"
    if not os.path.exists(file_path):
        return False
    os.remove(file_path)
    return True


# 根据文件路径信息拼接文件路径
def get_file_path(item: models.Item, user: schemas.User) -> str:
    file_path = ""
    while item.parent_id != 0:
        parent_item: models.Item = crud.get_item(item.parent_id)
        file_path: str = f"{parent_item.name}/{file_path}"
        item = parent_item
    return f"{get_root_path(user)}/{file_path}{item.name}"


# 创建用户根文件夹
def create_root_folder(
    path: str,
    user: schemas.User,
    # user: schemas.User = Depends(get_current_active_user),
    db: Session,
) -> bool:
    print("create folder")
    user_root_path = get_root_path(user)
    print(user_root_path)
    item_create = schemas.ItemCreate(path=path, type=0, size=0)
    # if path != "" and (not os.path.exists(f"{user_root_path}")):
    #    raise Exception("user root path not exists")
    os.mkdir(f"{user_root_path}/{path}")
    crud.create_user_root_item(db, item_create, user)
    return True


def create_folder(
    path: str,
    user: schemas.User,
    # user: schemas.User = Depends(get_current_active_user),
    db: Session,
) -> bool:
    print("create folder")
    user_root_path = get_root_path(user)
    print(user_root_path)
    item_create = schemas.ItemCreate(path=path, type=0, size=0)
    # if path != "" and (not os.path.exists(f"{user_root_path}")):
    #    raise Exception("user root path not exists")
    os.mkdir(f"{user_root_path}/{path}")
    crud.create_user_item(db, item_create, user)
    return True


'''def get_file_path(item: Item, user: User) -> str:
    if item.parent_id == 0:
        return f"{get_root_path(user)}/{item.name}"
    else:
        return get_file_path(get_item(item.parent_id), user) + f"/{item.name}"'''
