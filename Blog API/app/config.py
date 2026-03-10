from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    database_url: str = Field(
        default="mongodb://localhost:27017",
        alias="MONGO_URI",
        description="Mongodb connection string"
    )

    db_name: str = Field(
        default="mydb",
        alias="DB_NAME",
        description="Database name"
    )

    model_config = SettingsConfigDict(
        extra='forbid'
    )

settings = Settings()