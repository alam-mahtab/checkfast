from sqlalchemy.orm import Session
from . import models, schemas

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional

def create_tutor(db: Session,title:str,name:str,desc:str,url:str):
    db_tutor = models.Tutor(title=title,desc=desc,name=name,url=url)
    db.add(db_tutor)
    db.commit()
    db.refresh(db_tutor)
    return db_tutor

def get_tutor(db, id: int):
    return db.query(models.Tutor).filter(models.Tutor.id== id).first()

def tutor_list(db):
    return db.query(models.Tutor).all()

async def delete(db: Session,id: int)-> bool:
   sym1 =models.Tutor.__table__
   sym = sym1.delete().where(models.Tutor.id== id)
   print(sym)
   result = db.execute(sym)
   db.commit()
   return True