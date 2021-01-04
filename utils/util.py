from configs.connection import database
from passlib.context import CryptContext
from datetime import datetime, timedelta
from utils import constant
import jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def findExistedUser(username : str):
    
    query = " select * from users where status='1' and username=:username "

    return database.fetch_one(query, values={ "username" : username})

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, constant.SECRET_KEY, algorithm=constant.ALGORITHM)
    return encoded_jwt
