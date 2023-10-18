from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from .api import file, users
from .db import models
from .db.database import engine
from .dependencies import get_db

# 判断数据库是否为空，如果为空则初始化数据库
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(users.router)
app.include_router(file.router)


@app.get("/")
async def read_root():
    # init_dababase(db)
    return {"Hello": "World"}
