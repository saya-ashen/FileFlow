import os
from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel

from ..db import crud, models, schemas
from ..db.schemas import FileInfo
from ..dependencies import oauth2_scheme

# 定义文件系统根目录
root = "./root"

router = APIRouter(prefix="/api")


@router.post("/api/mkdir/{path:path}")
def mkdir(path: str):
    if not os.path.exists(f"{root}/{path}"):
        return {"error": "path not exists"}
    os.mkdir(f"{root}/{path}")
    return {"path": path}


@router.post("/api/move/{path:path}")
def move(path: str):
    if not os.path.exists(f"{root}/{path}"):
        return {"error": "path not exists"}
    os.mkdir(f"{root}/{path}")
    return {"path": path}


@router.post("/api/copy/{path:path}")
def copy(path: str):
    if not os.path.exists(f"{root}/{path}"):
        return {"error": "path not exists"}
    os.mkdir(f"{root}/{path}")
    return {"path": path}


@router.post("/api/delete/{path:path}")
def delete(path: str):
    if not os.path.exists(f"{root}/{path}"):
        return {"error": "path not exists"}
    os.mkdir(f"{root}/{path}")
    return {"path": path}


@router.post("/api/rename/{path:path}")
def rename(path: str):
    if not os.path.exists(f"{root}/{path}"):
        return {"error": "path not exists"}
    os.mkdir(f"{root}/{path}")
    return {"path": path}


# 上传文件之前先发送json数据，包括文件名，文件大小，文件类型，文件路径等信息
@router.post("/api/preupload/{path:path}")
def preupload(fileinfo: FileInfo, path: str):
    fileinfo.path = path
    # 判断文件夹路径是否存在，如果不存在则返回错误信息
    if not os.path.exists(f"{root}/{path}"):
        return {"error": "path not exists"}

    return {"path": path}


# 上传文件，实现断点续传功能？
@router.post("/api/upload/{path:path}")
async def create_upload_file(file: UploadFile, fileinfo: FileInfo, path: str):
    contents = await file.read()
    if not os.path.exists(f"{root}/{path}"):
        return {"error": "path not exists"}

    with open(f"{root}/{path}/{file.filename}", "wb") as f:
        f.write(contents)
    return {"filename": file.filename}


@router.get("/api/list/{path:path}")
async def list(path: str, token: Annotated[str, Depends(oauth2_scheme)]):
    print("token", token)
    if not os.path.exists(f"{root}/{path}"):
        return {"error": "path not exists"}
    return os.listdir(f"{root}/{path}")


@router.get("/api/download/{path:path}")
async def download(path: str):
    if not os.path.exists(f"{root}/{path}"):
        return {"error": "path not exists"}
    return FileResponse(f"{root}/{path}")
