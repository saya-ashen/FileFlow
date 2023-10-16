import os

from pydantic_settings import BaseSettings, SettingsConfigDict
from yarl import URL


class Settings(BaseSettings):
    """db_host: str = "localhost"
    db_port: int = 3306
    db_user: str = "fileflow"
    db_pass: str = "fileflow"
    db_base: str = "fileflow"
    db_echo: bool = False"""

    ROOT_PATH: str = "/root/workspace/fileflow/backend"
    SQLALCHEMY_DATABASE_URL: str = f"sqlite:///{ROOT_PATH}/db/sql.db"
    DEFAULT_CAPACITY: int = 1024 * 1024 * 1024 * 1024
    # SECRET_KEY: str = "b3d6e"
    ALGORITHM: str = "HS256"
    TOKEN_URL: str = "/api/login"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    JWT_SECRET_KEY: str = "test"  # should be kept secret
    JWT_REFRESH_SECRET_KEY: str = "test"  # should be kept secret

    @property
    def db_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.
        """
        """return URL.build(
            scheme="sqlite",
            # host=self.db_host,
            # port=self.db_port,
            # user=self.db_user,
            # password=self.db_pass,
            path=f"/{self.db_base}",
        )"""
        return self.SQLALCHEMY_DATABASE_URL

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="FILEFLOW_",
        env_file_encoding="utf-8",
    )


settings = Settings()
