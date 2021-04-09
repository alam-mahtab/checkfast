from pydantic import BaseSettings

class setting(BaseSettings):
    AWS_ACCESS_KEY_ID : str
    AWS_SECRET_ACCESS_KEY : str
    AWS_REGION :str
    S3_Bucket : str
    

    class Config:
        env_file = "app/.env"