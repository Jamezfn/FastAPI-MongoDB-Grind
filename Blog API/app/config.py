from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr

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

    jwt_secret: SecretStr = Field(
        alias='JWT_SECRET',
        description="Secret key for JWT token signing (min 32 chars)",
        min_length=32
    )

    jwt_algorithm: str = Field(
        default="HS256",
        alias='JWT_ALGORITHMN',
        description="JWT signing algorithm",
        pattern='^(HS256|RS256|HS512)$'
    )

    model_config = SettingsConfigDict(
        extra='forbid',
        env_file='.env'
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

settings = Settings()