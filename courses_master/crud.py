
from sqlalchemy.orm import Session
from . import models, schemas, database
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional

def create_master(db: Session,title:str,name:str,desc:str,url:str):
    db_master = models.Master(title=title,desc=desc,name=name,url=url)
    db.add(db_master)
    db.commit()
    db.refresh(db_master)
    return db_master

def get_master(db, id: int):
    return db.query(models.Master).filter(models.Master.id== id).first()

def master_list(db):
    return db.query(models.Master).all()