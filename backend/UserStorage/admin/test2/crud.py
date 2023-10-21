import os

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from ..settings import settings
from ..utils import create_folder
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
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    # 创建用户根目录
    create_folder(user.username, db_user, db)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()


# 按照文件名查找文件夹下的特定文件
def get_item_by_name(db: Session, name: str, parent_id: int):
    return (
        db.query(models.Item)
        .filter(models.Item.name == name, models.Item.parent_id == parent_id)
        .first()
    )


# 根据文件（夹）路径获取文件（夹）信息
def get_item_by_path(db: Session, path: str):
    # 将传递的路径信息拆分为目录名称的列表
    path_parts = path.split("/")
    if len(path_parts) == 1:
        return db.query(models.Item).filter(models.Item.name == path).first()
    # 初始化根目录的ID
    parent_id = 0

    for folder_name in path_parts:
        folder_id = get_item_by_name(db, folder_name, parent_id)
        if folder_id is None:
            raise Exception("path not exists")
        parent_id = folder_id

    return db.query(models.Item).filter(models.Item.path == path).first()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    parent = get_item_by_path(db, item.path)
    name = item.path.split("/")[-1]
    db_item = models.Item(
        **item.model_dump(),
        owner_id=user_id,
        parent_id=parent.id,
        type=item.type,
        size=item.size,
        name=name,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def init_dababase(db: Session):
    print("init database")
    admin = schemas.UserCreate(
        email="admin@admin", nickname="admin", username="admin", password="admin123"
    )
    # 判断根目录是否存在，如果不存在则创建
    if not os.path.exists(settings.ROOT_PATH + "/UserStorage"):
        os.mkdir(settings.ROOT_PATH + "/UserStorage")
    admin_user = create_user(db, admin)
    print(admin_user)


# 判断剩余空间是否足够
def check_space(db: Session, user_id: int, size: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user.space - size < 0:
        return False
    else:
        return True
