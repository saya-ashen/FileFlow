import os
from datetime import datetime, timedelta
from typing import Any, Union

from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from .db import crud, models, schemas
from .settings import settings

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_token(
    subject: Union[str, Any], expires_delta: timedelta = None, is_access: bool = True
):
    # 如果没有提供 expires_delta，我们将根据是访问令牌还是刷新令牌来设置默认值
    if expires_delta is None:
        if is_access:
            expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        else:
            expires_delta = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    expires = datetime.utcnow() + expires_delta

    to_encode = {"exp": expires, "sub": str(subject)}
    if is_access:
        secret_key = settings.JWT_SECRET_KEY
    else:
        secret_key = settings.JWT_REFRESH_SECRET_KEY

    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=settings.ALGORITHM)

    # 将过期时间转换为特定格式的字符串
    expires_str = expires.strftime("%Y/%m/%d %H:%M:%S")

    # 返回 token 和格式化的过期时间字符串
    return encoded_jwt, expires_str


# 创建访问令牌的函数
def create_access_token(*args, **kwargs) -> dict:
    token, expires = create_token(*args, is_access=True, **kwargs)
    return token, expires


# 创建刷新令牌的函数
def create_refresh_token(*args, **kwargs) -> dict:
    token, expires = create_token(*args, is_access=False, **kwargs)
    return token, expires


def verify_refresh_token(token: str):
    """
    验证刷新令牌并返回令牌中的数据。
    如果验证失败，返回 None。
    """
    try:
        payload = jwt.decode(
            token, settings.JWT_REFRESH_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload

    except ExpiredSignatureError:
        # 如果令牌已过期
        print("Refresh token has expired")
        return None

    except JWTError as e:
        # 其他类型的异常
        print(f"An error occurred: {e}")
        return None


"""def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
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
    return encoded_jwt"""


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
