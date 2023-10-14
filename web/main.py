from fastapi import FastAPI

from .api import file, users
from .db import models
from .db.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(users.router)
app.include_router(file.router)


@app.get("/")
async def read_root():
    return {"Hello": "World"}
