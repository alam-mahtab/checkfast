from sqlalchemy.orm import Session
from . import models, schemas

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional

def create_filmo(db: Session,title:str,desc:str,url:str,status:int):
    db_filmo = models.Filmo(title=title,desc=desc,url=url,status=status)
    db.add(db_filmo)
    db.commit()
    db.refresh(db_filmo)
    return db_filmo

def get_filmo(db, id: int):
    return db.query(models.Filmo).filter(models.Filmo.id== id).first()

def filmo_list(db):
    return db.query(models.Filmo).all()

async def delete(db: Session,id: int)-> bool:
   sym1 =models.Filmo.__table__
   sym = sym1.delete().where(models.Filmo.id== id)
   print(sym)
   result = db.execute(sym)
   db.commit()
   return True