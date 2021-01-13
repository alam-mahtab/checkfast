
from sqlalchemy.orm import Session
from . import models, schemas
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional

def create_director(db: Session,name:str,desc:str,url_profile:str, url_cover:str):
    db_director = models.Director (name=name,desc=desc,url_profile=url_profile,url_cover=url_cover)
    db.add(db_director)
    db.commit()
    db.refresh(db_director)
    return db_director


def get_director(db, id: int):
    return db.query(models.Director).filter(models.Director.id== id).first()

def director_list(db):
    return db.query(models.Director).all()

async def delete(db: Session,id: int)-> bool:
   sym1 =models.Director.__table__
   sym = sym1.delete().where(models.Director.id== id)
   print(sym)
   result = db.execute(sym)
   db.commit()
   return True