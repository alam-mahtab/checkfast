
from sqlalchemy.orm import Session
from . import models, schemas
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional

def create_cinematographer(db: Session,name:str,desc:str,url_profile:str, url_cover:str):
    db_cinemato = models.Cinematographer(name=name,desc=desc,url_profile=url_profile,url_cover=url_cover)
    db.add(db_cinemato)
    db.commit()
    db.refresh(db_cinemato)
    return db_cinemato


def get_cinematographer(db, id: int):
    return db.query(models.Cinematographer).filter(models.Cinematographer.id== id).first()

def cinematographer_list(db):
    return db.query(models.Cinematographer).all()

async def delete(db: Session,id: int)-> bool:
   sym1 =models.Cinematographer.__table__
   sym = sym1.delete().where(models.Cinematographer.id== id)
   print(sym)
   result = db.execute(sym)
   db.commit()
   return True