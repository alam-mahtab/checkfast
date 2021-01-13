
from sqlalchemy.orm import Session
from . import models, schemas
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional

def create_videographer(db: Session,name:str,desc:str,url_profile:str, url_cover:str):
    db_videographer = models.Video(name=name,desc=desc,url_profile=url_profile,url_cover=url_cover)
    db.add(db_videographer)
    db.commit()
    db.refresh(db_videographer)
    return db_videographer


def get_videographer(db, id: int):
    return db.query(models.Video).filter(models.Video.id== id).first()

def videographer_list(db):
    return db.query(models.Video).all()

async def delete(db: Session,id: int)-> bool:
   sym1 =models.Video.__table__
   sym = sym1.delete().where(models.Video.id== id)
   print(sym)
   result = db.execute(sym)
   db.commit()
   return True