from pydantic import BaseSettings

class setting(BaseSettings):
    TWITTER_CLIENT_ID : str
    TWITTER_CLIENT_SECRET : str
    

    class Config:
        env_file = "app/.env"