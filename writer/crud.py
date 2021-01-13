
from sqlalchemy.orm import Session
from . import models, schemas, database
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional

def create_writer(db: Session,name:str,desc:str,url_profile:str, url_cover:str):
    db_writer = models.Writer(name=name,desc=desc,url_profile=url_profile,url_cover=url_cover)
    db.add(db_writer)
    db.commit()
    db.refresh(db_writer)
    return db_writer


def get_writer(db, id: int):
    return db.query(models.Writer).filter(models.Writer.id== id).first()

def writer_list(db):
    return db.query(models.Writer).all()

async def delete(db: Session,id: int)-> bool:
   sym1 =models.Writer.__table__
   sym = sym1.delete().where(models.Writer.id== id)
   print(sym)
   result = db.execute(sym)
   db.commit()
   return True