from pydantic import BaseSettings

class setting(BaseSettings):
    email_id : str
    email_pwd: str
    

    class Config:
        env_file = "app/.env"