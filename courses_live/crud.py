from sqlalchemy.orm import Session
from . import models, schemas, database

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional

def create_post(db: Session,title:str,name:str,desc:str,url:str):
    db_post = models.Post(title=title,desc=desc,name=name,url=url)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_post(db, id: int):
    return db.query(models.Post).filter(models.Post.id== id).first()

def post_list(db):
    return db.query(models.Post).all()