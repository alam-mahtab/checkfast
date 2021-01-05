from configs.connection import database
from passlib.context import CryptContext
from datetime import datetime, timedelta
from utils import constant
import jwt
from fastapi import HTTPException, Depends, status,  File, Form, UploadFile
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from auth import model
from jwt import PyJWTError
from pydantic import ValidationError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


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

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, constant.SECRET_KEY, algorithms=[constant.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = model.TokenData(username=username)
    except (PyJWTError, ValidationError):
        raise credentials_exception
    user = await findExistedUser(token_data.username)
    #user = constant.get_user(db, username=token_data)
    if user is None:
        raise credentials_exception
    return user
    #return model.UserList(**user)

async def get_current_active_user(current_user: model.UserList = Depends(get_current_user)):
    if current_user.status == "9":
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
# New
async def create_file(
    file: bytes = File(...), fileb: UploadFile = File(...), token: str = Form(...)
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,}