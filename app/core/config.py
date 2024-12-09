from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "FastAPI Project"
    database_url: str
    secret_key: str

    class Config:
        env_file = ".env"


settings = Settings()
