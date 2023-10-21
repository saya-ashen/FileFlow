import os
from typing import Dict, List

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from ..db import crud, models
from ..db.schemas import ItemCreate, User
from ..dependencies import create_folder_dp, get_current_active_user, get_db
from ..utils import get_file_path, get_root_path

router = APIRouter(prefix="/api")

# 定义储存用户文件的根目录


@router.post("/mkdir/{path:path}")
def mkdir(
    success: bool = Depends(create_folder_dp),
):
    return {"success": success}


@router.post("/rename/{path:path}")
def rename(
    path: str,
    target: ItemCreate,
    action: str,
    destination: str,
    override: bool,
    rename: bool,
    user: User = Depends(get_current_active_user),
):
    user_root_path = get_root_path(user)
    if not os.path.exists(f"{user_root_path}/{path}"):
        return {"error": "path not exists"}
    return {"path": path}


@router.post("/copy/{path:path}")
def copy(path: str, user: User = Depends(get_current_active_user)):
    user_root_path = get_root_path(user)
    if not os.path.exists(f"{user_root_path}/{path}"):
        return {"error": "path not exists"}
    os.mkdir(f"{user_root_path}/{path}")
    return {"path": path}


@router.post("/delete/{path:path}")
def delete(path: str, user: User = Depends(get_current_active_user)):
    user_root_path = get_root_path(user)
    file_path = f"{user_root_path}/{path}"
    if not os.path.exists(file_path):
        return {"error": "path not exists"}
    # 删除文件或文件夹
    if os.path.isfile(file_path):
        os.remove(file_path)
    else:
        os.rmdir(file_path)
    return {"path": path}


@router.post("/rename/{path:path}")
def rename(path: str, user: User = Depends(get_current_active_user)):
    user_root_path = get_root_path(user)
    if not os.path.exists(f"{user_root_path}/{path}"):
        return {"error": "path not exists"}
    os.mkdir(f"{user_root_path}/{path}")
    return {"path": path}


# 上传文件之前先发送json数据，包括文件名，文件大小，文件类型，文件路径等信息
@router.post("/preupload/{path:path}")
async def preupload(
    itemcreate: ItemCreate,
    path: str = None,
    user: User = Depends(get_current_active_user),
):
    user_root_path = get_root_path(user)
    # 判断文件夹路径是否存在，如果不存在则返回错误信息
    if not os.path.exists(f"{user_root_path}/{path}"):
        print(f"{user_root_path}/{path}")
        return {"error": "path not exists"}
    # 判断剩余空间是否足够，如果不够则返回错误信息
    if not crud.check_space(user.id, itemcreate.size):
        return {"error": "space not enough"}

    return {"path": path}


# 上传文件，实现断点续传功能？
@router.post("/upload")
async def upload(
    folder_id: int = Query(-1),
    file: UploadFile = File(...),
    user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    if folder_id == -1:
        folder = crud.get_user_item_by_path(db, user, "/")
    else:
        # 判断所给的folder_id是否有效
        folder = crud.get_item(db, folder_id)
        if folder is None:
            return {"error": "path not exists"}
        if folder.owner_id != user.id:
            return {"error": "permission denied"}
        if folder.type != 0:
            return {"error": "not a folder"}

    # 获取文件夹路径并判断是否存在
    path_relative = get_file_path(db, folder, user, relative=True)
    path_full = get_root_path(user) + "/" + path_relative
    contents = await file.read()
    if not os.path.exists(path_full):
        return {"error": "path not exists"}

    # 写入文件并将文件信息写入数据库
    with open(f"{path_full}/{file.filename}", "wb") as f:
        f.write(contents)
    item = ItemCreate(
        path=f"{path_relative}/{file.filename}",
        type=1,
        size=file.size,
    )
    crud.create_user_item(db, item, user)
    return {"filename": file.filename, "success": True}


@router.get("/list")
async def list(
    item_id: int = Query(-1),
    user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    if item_id == -1:
        folder = crud.get_user_item_by_path(db, user, "/")
        items = crud.get_items_by_parent_id(db, folder.id)
    else:
        folder = crud.get_item(db, item_id)
        # folder = crud.get_user_item_by_path(db, user, path)
        if folder is None:
            return {"error": "path not exists"}
        if folder.owner_id != user.id:
            return {"error": "permission denied"}
        items = crud.get_items_by_parent_id(db, folder.id)
        parent = crud.get_item(db, folder.parent_id)
        if parent is not None:
            items.append(
                models.Item(
                    id=parent.id,
                    name="..",
                    type=0,
                    size=0,
                    parent_id=parent.parent_id,
                    owner_id=parent.owner_id,
                )
            )
    items.append(
        models.Item(
            id=folder.id,
            name=".",
            type=0,
            size=0,
            parent_id=folder.parent_id,
            owner_id=folder.owner_id,
        )
    )
    response = {"items": items, "total": len(items), "success": True}
    return response


@router.get("/download/{path:path}")
async def download(
    path: str, files: List[str] = Query(), user: User = Depends(get_current_active_user)
):
    """
    暂时只支持下载单个文件，选择多个文件下载时，只下载第一个文件
    """
    user_root_path = get_root_path(user)
    files_path = []
    for file in files:
        if not os.path.exists(f"{user_root_path}/{path}/{file}"):
            return {"error": "path not exists"}
        files_path.append(f"{user_root_path}/{path}/{file}")
    return FileResponse(files_path[0])
