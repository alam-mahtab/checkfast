
from sqlalchemy.orm import Session
from . import models, schemas
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional

def create_sound(db: Session,name:str,desc:str,url_profile:str, url_cover:str):
    db_sound = models.Sound(name=name,desc=desc,url_profile=url_profile,url_cover=url_cover)
    db.add(db_sound)
    db.commit()
    db.refresh(db_sound)
    return db_sound


def get_sound(db, id: int):
    return db.query(models.Sound).filter(models.Sound.id== id).first()

def sound_list(db):
    return db.query(models.Sound).all()

async def delete(db: Session,id: int)-> bool:
   sym1 =models.Sound.__table__
   sym = sym1.delete().where(models.Sound.id== id)
   print(sym)
   result = db.execute(sym)
   db.commit()
   return True