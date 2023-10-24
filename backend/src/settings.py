from pydantic import Field
from pydantic_settings import BaseSettings


# 从环境变量中读取配置
class Settings(BaseSettings):
    ROOT_PATH: str = "/usr/src/app"
    # ROOT_PATH: str = "/root/workspace/fileflow/backend"
    SQLALCHEMY_DATABASE_URL: str = f"sqlite:///{ROOT_PATH}/src/db/sql.db"
    DEFAULT_CAPACITY: int = Field(1024 * 1024 * 1024 * 1024, env="DEFAULT_CAPACITY")
    ALGORITHM: str = Field("HS256", env="ALGORITHM")
    TOKEN_URL: str = "/api/login"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_MINUTES: int = Field(
        60 * 24 * 7, env="REFRESH_TOKEN_EXPIRE_MINUTES"
    )
    JWT_SECRET_KEY: str = Field("test", env="JWT_SECRET_KEY")
    JWT_REFRESH_SECRET_KEY: str = Field("test", env="JWT_REFRESH_SECRET_KEY")

    @property
    def db_url(self):
        return self.SQLALCHEMY_DATABASE_URL

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
