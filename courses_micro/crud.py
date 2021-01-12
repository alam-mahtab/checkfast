
from sqlalchemy.orm import Session
from . import models, schemas, database
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional

def create_micro(db: Session,title:str,name:str,desc:str,url:str):
    db_micro = models.Micro(title=title,desc=desc,name=name,url=url)
    db.add(db_micro)
    db.commit()
    db.refresh(db_micro)
    return db_micro

def get_micro(db, id: int):
    return db.query(models.Micro).filter(models.Micro.id== id).first()

def micro_list(db):
    return db.query(models.Micro).all()

    
async def delete(db: Session,id: int)-> bool:
   sym1 =models.Micro.__table__
   sym = sym1.delete().where(models.Micro.id== id)
   print(sym)
   result = db.execute(sym)
   db.commit()
   return True
