import os

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from ..settings import settings
from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    # 生成加密后的密码
    password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = password_context.hash(user.password)
    root_path = settings.ROOT_PATH + "/UserStorage/" + user.username
    # 判断root_path是否存在，如果不存在则创建, 如果存在则返回错误信息
    if not os.path.exists(root_path):
        os.mkdir(root_path)
    else:
        return {"error": "username exists"}
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        username=user.username,
        nickname=user.nickname,
        capacity=settings.DEFAULT_CAPACITY,
        used=0,
        is_active=True,
        role=1,
        root_path=root_path,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# 判断剩余空间是否足够
def check_space(db: Session, user_id: int, size: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user.space - size < 0:
        return False
    else:
        return True
