from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings

class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000

class ApiPrefix(BaseModel):
    prefix: str = "/api"

class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    max_overflow: int = 50
    pool_size: int = 10

class Settings(BaseSettings):
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig

settings = Settings()
