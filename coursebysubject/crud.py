from sqlalchemy.orm import Session
from . import models, schemas

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional

def create_subject(db: Session,title:str,name:str,desc:str,url:str):
    db_subject = models.Subject(title=title,desc=desc,name=name,url=url)
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject

def get_subject(db, id: int):
    return db.query(models.Subject).filter(models.Subject.id== id).first()

def subject_list(db):
    return db.query(models.Subject).all()