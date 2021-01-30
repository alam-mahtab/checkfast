from sqlalchemy.orm import Session
from . import models, schemas

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional

def create_award(db: Session,title:str,desc:str,url:str,status:int):
    db_award = models.Award(title=title,desc=desc,url=url,status=status)
    db.add(db_award)
    db.commit()
    db.refresh(db_award)
    return db_award

def get_award(db, id: int):
    return db.query(models.Award).filter(models.Award.id== id).first()

def award_list(db):
    return db.query(models.Award).all()

async def delete(db: Session,id: int)-> bool:
   sym1 =models.Award.__table__
   sym = sym1.delete().where(models.Award.id== id)
   print(sym)
   result = db.execute(sym)
   db.commit()
   return True