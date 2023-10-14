from fileflow.settings import settings
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from . import models
from .database import SessionLocal


async def create_database() -> None:
    engine = create_async_engine(settings.db_url)

    # 检查数据库是否存在，如果不存在则创建
    db = SessionLocal()
    try:
        # 通过执行一个数据库查询来检查数据库是否存在
        db.execute("SELECT 1")
    except Exception as e:
        # 如果查询失败，表示数据库不存在，创建数据库表
        print(e)
        models.Base.metadata.create_all(bind=engine)

    finally:
        db.close()

    """async with engine.connect() as conn:
        database_existance = await conn.execute(
            text(
                "SELECT 1 FROM INFORMATION_SCHEMA.SCHEMATA"  # noqa: S608
                f" WHERE SCHEMA_NAME='{settings.db_base}';",
            ),
        )
        database_exists = database_existance.scalar() == 1

    if database_exists:
        await drop_database()"""

    async with engine.connect() as conn:  # noqa: WPS440
        await conn.execute(
            text(
                f"CREATE DATABASE {settings.db_base};",
            ),
        )
    raise NotImplementedError


async def drop_database() -> None:
    """Drop current database."""
    engine = create_async_engine(settings.db_url)
    async with engine.connect() as conn:
        await conn.execute(text(f"DROP DATABASE {settings.db_base};"))
