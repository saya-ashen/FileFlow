from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    # 用户的用户名
    username = Column(String, unique=True, index=True)
    # 用户的昵称
    nickname = Column(String, index=True)
    # 用户的邮箱
    email = Column(String, unique=True, index=True)
    # 用户的存储空间，单位为字节
    capacity = Column(Integer, default=0)
    # 用户已经使用的存储空间，单位为字节
    used = Column(Integer, default=0)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    # 文件类型，0表示文件，1表示文件夹
    type = Column(Integer, index=True, default=0)
    # 文件大小，单位为字节
    size = Column(Integer, index=True, default=0)
    # 文件的父文件夹
    parent = Column(Integer, index=True, default=0)
    # 文件的路径
    path = Column(String, index=True, default="")
    # 文件的所有者
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")
