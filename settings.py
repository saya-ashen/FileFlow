from pydantic_settings import BaseSettings, SettingsConfigDict
from yarl import URL


class Settings(BaseSettings):
    db_host: str = "localhost"
    db_port: int = 3306
    db_user: str = "fileflow"
    db_pass: str = "fileflow"
    db_base: str = "fileflow"
    db_echo: bool = False

    ROOT_PATH: str = "/root/workspace/fileflow"
    SQLALCHEMY_DATABASE_URL: str = f"sqlite:///{ROOT_PATH}/web/db/sql.db"

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
print(settings.db_url)
