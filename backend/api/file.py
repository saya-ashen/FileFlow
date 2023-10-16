import os
from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from ..db.crud import check_space
from ..db.schemas import ItemCreate, User
from ..dependencies import get_current_active_user, get_db, oauth2_scheme
from ..settings import settings
from ..utils import get_root_path

router = APIRouter(prefix="/api")

# 定义储存用户文件的根目录


@router.post("/mkdir/{path:path}")
def mkdir(
    path: str,
    user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    user_root_path = get_root_path(user)
    if not os.path.exists(f"{user_root_path}/{path}"):
        return {"error": "path not exists"}
    os.mkdir(f"{user_root_path}/{path}")
    return {"path": path}


@router.post("/move/{path:path}")
def move(path: str):
    user_root_path = get_root_path(user)
    if not os.path.exists(f"{user_root_path}/{path}"):
        return {"error": "path not exists"}
    os.mkdir(f"{user_root_path}/{path}")
    return {"path": path}


@router.post("/copy/{path:path}")
def copy(path: str):
    user_root_path = get_root_path(user)
    if not os.path.exists(f"{user_root_path}/{path}"):
        return {"error": "path not exists"}
    os.mkdir(f"{user_root_path}/{path}")
    return {"path": path}


@router.post("/delete/{path:path}")
def delete(path: str):
    user_root_path = get_root_path(user)
    if not os.path.exists(f"{user_root_path}/{path}"):
        return {"error": "path not exists"}
    os.mkdir(f"{user_root_path}/{path}")
    return {"path": path}


@router.post("/rename/{path:path}")
def rename(path: str):
    user_root_path = get_root_path(user)
    if not os.path.exists(f"{user_root_path}/{path}"):
        return {"error": "path not exists"}
    os.mkdir(f"{user_root_path}/{path}")
    return {"path": path}


# 上传文件之前先发送json数据，包括文件名，文件大小，文件类型，文件路径等信息
@router.post("/preupload/{path:path}|/preupload")
async def preupload(
    itemcreate: ItemCreate,
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
    path: str = None,
):
    user_root_path = get_root_path(user)
    # 判断文件夹路径是否存在，如果不存在则返回错误信息
    if not os.path.exists(f"{user_root_path}/{path}"):
        print(f"{user_root_path}/{path}")
        return {"error": "path not exists"}
    # 判断剩余空间是否足够，如果不够则返回错误信息
    user = await get_current_active_user(db, token)
    if not check_space(user.id, itemcreate.size):
        return {"error": "space not enough"}

    return {"path": path}


# 上传文件，实现断点续传功能？
@router.post("/upload/{path:path}")
async def create_upload_file(file: UploadFile, itemCreate: ItemCreate, path: str):
    user_root_path = get_root_path(user)
    contents = await file.read()
    if not os.path.exists(f"{user_root_path}/{path}"):
        return {"error": "path not exists"}

    with open(f"{user_root_path}/{path}/{file.filename}", "wb") as f:
        f.write(contents)
    return {"filename": file.filename}


@router.get("/list/{path:path}")
async def list(path: str, user: User = Depends(get_current_active_user)):
    user_root_path = get_root_path(user)
    if not os.path.exists(f"{user_root_path}/{path}"):
        return {"error": "path not exists"}
    return os.listdir(f"{user_root_path}/{path}")


@router.get("/download/{path:path}")
async def download(path: str):
    user_root_path = get_root_path(user)
    if not os.path.exists(f"{user_root_path}/{path}"):
        return {"error": "path not exists"}
    return FileResponse(f"{user_root_path}/{path}")
