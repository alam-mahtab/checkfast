from pydantic import BaseSettings

class setting(BaseSettings):
    GOOGLE_CLIENT_ID : str
    GOOGLE_CLIENT_SECRET : str
    

    class Config:
        env_file = "app/.env"