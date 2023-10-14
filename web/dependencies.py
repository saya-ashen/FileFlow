from fastapi.security import OAuth2PasswordBearer

from .db import crud, models, schemas
from .db.database import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
