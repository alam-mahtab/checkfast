from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import user
#from . import model, schemas
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from db.table import Users
from utils import util, constant

def create_user(db: Session,username:str,email:str,first_name:str,last_name:str,dateofbirth:str,status:str,phone:str,
    password:str,confirm_password:str):
    db_user = Users(username=username,email=email,password=password,confirm_password=confirm_password,
    first_name=first_name,last_name=last_name,dateofbirth=dateofbirth,phone=phone,status=status)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user