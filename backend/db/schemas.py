from pydantic import BaseModel


class ItemBase(BaseModel):
    # 类型 0 文件夹 1 文件
    type: int
    size: int


class ItemCreate(ItemBase):
    path: str
    pass


class Item(ItemBase):
    id: int
    name: str
    parent_id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str
    nickname: str | None = None
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    role: int
    nickname: str
    email: str
    capacity: int
    used: int
    username: str
    items: list[Item] = []

    class Config:
        orm_mode = True


class Item(BaseModel):
    id: int
    name: str
    type: int
    size: int
    parent: int
    path: str
    owner_id: int

    class Config:
        orm_mode = True
