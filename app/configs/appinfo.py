from pydantic import BaseSettings

class setting(BaseSettings):
    app_name : str
    app_version: str
    app_framework : str
    app_date : str

    class Config:
        env_file = "app/.env"