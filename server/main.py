import os

from fastapi import FastAPI, File, UploadFile

# 定义文件系统根目录
root = "./root"

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/api/upload{path}")
async def create_upload_file(file: UploadFile, path: str):
    contents = await file.read()
    if not os.path.exists(f"{root}/{path}"):
        return {"error": "path not exists"}
    with open(f"{root}/{path}/{file.filename}", "wb") as f:
        f.write(contents)
    return {"filename": file.filename}
