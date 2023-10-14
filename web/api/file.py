import os
from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from ...settings import settings
from ..db.crud import check_space
from ..db.schemas import ItemCreate
from ..dependencies import get_current_active_user, get_db, oauth2_scheme

# 定义文件系统根目录
root = f"{settings.ROOT_PATH}/web/root"

router = APIRouter(prefix="/api")


@router.post("/mkdir/{path:path}")
def mkdir(path: str):
    if not os.path.exists(f"{root}/{path}"):
        return {"error": "path not exists"}
    os.mkdir(f"{root}/{path}")
    return {"path": path}


@router.post("/move/{path:path}")
def move(path: str):
    if not os.path.exists(f"{root}/{path}"):
        return {"error": "path not exists"}
    os.mkdir(f"{root}/{path}")
    return {"path": path}


@router.post("/copy/{path:path}")
def copy(path: str):
    if not os.path.exists(f"{root}/{path}"):
        return {"error": "path not exists"}
    os.mkdir(f"{root}/{path}")
    return {"path": path}


@router.post("/delete/{path:path}")
def delete(path: str):
    if not os.path.exists(f"{root}/{path}"):
        return {"error": "path not exists"}
    os.mkdir(f"{root}/{path}")
    return {"path": path}


@router.post("/rename/{path:path}")
def rename(path: str):
    if not os.path.exists(f"{root}/{path}"):
        return {"error": "path not exists"}
    os.mkdir(f"{root}/{path}")
    return {"path": path}


# 上传文件之前先发送json数据，包括文件名，文件大小，文件类型，文件路径等信息
@router.post("/preupload/{path:path}|/preupload")
async def preupload(
    itemcreate: ItemCreate,
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
    path: str = None,
):
    # 判断文件夹路径是否存在，如果不存在则返回错误信息
    if not os.path.exists(f"{root}/{path}"):
        print(f"{root}/{path}")
        return {"error": "path not exists"}
    # 判断剩余空间是否足够，如果不够则返回错误信息
    user = await get_current_active_user(db, token)
    if not check_space(user.id, itemcreate.size):
        return {"error": "space not enough"}

    return {"path": path}


# 上传文件，实现断点续传功能？
@router.post("/upload/{path:path}")
async def create_upload_file(file: UploadFile, itemCreate: ItemCreate, path: str):
    contents = await file.read()
    if not os.path.exists(f"{root}/{path}"):
        return {"error": "path not exists"}

    with open(f"{root}/{path}/{file.filename}", "wb") as f:
        f.write(contents)
    return {"filename": file.filename}


@router.get("/list/{path:path}")
async def list(path: str, token: Annotated[str, Depends(oauth2_scheme)]):
    print("token", token)
    if not os.path.exists(f"{root}/{path}"):
        return {"error": "path not exists"}
    return os.listdir(f"{root}/{path}")


@router.get("/download/{path:path}")
async def download(path: str):
    if not os.path.exists(f"{root}/{path}"):
        return {"error": "path not exists"}
    return FileResponse(f"{root}/{path}")
