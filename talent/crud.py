
from sqlalchemy.orm import Session
from . import models, schemas, database
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional

def create_talent(db: Session,name:str,desc:str,type:str,status:int,url_profile:str, url_cover:str):
    db_talent = models.Talent(name=name,desc=desc,type=type,status=status,url_profile=url_profile,url_cover=url_cover)
    db.add(db_talent)
    db.commit()
    db.refresh(db_talent)
    return db_talent


def get_talent(db, id: int):
    return db.query(models.Talent).filter(models.Talent.id== id).first()

def talent_list(db):
    return db.query(models.Talent).all()

async def delete(db: Session,id: int)-> bool:
   sym1 =models.Talent.__table__
   sym = sym1.delete().where(models.Talent.id== id)
   print(sym)
   result = db.execute(sym)
   db.commit()
   return True

