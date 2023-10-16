from pydantic import BaseModel


class ItemBase(BaseModel):
    name: str
    type: int
    size: int


class ItemCreate(ItemBase):
    parent: int
    path: str


class Item(ItemBase):
    id: int
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
