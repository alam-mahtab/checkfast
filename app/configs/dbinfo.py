from pydantic import BaseSettings

class setting(BaseSettings):
    db_connection : str
    db_database : str
    db_stringlite :str
    db_stringpost : str
    

    class Config:
        env_file = "app/.env"