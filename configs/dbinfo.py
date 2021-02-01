from pydantic import BaseSettings

class setting(BaseSettings):
    db_connection : str
    db_database : str
    db_string : str
    

    class Config:
        env_file = "env"