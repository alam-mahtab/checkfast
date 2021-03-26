from sqlalchemy.orm import Session
from . import models, schemas

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional

def create_work(db: Session,name:str,email:str,message:str,status:int):
    db_work = models.Work(name=name,email=email,message=message,status=status)
    db.add(db_work)
    db.commit()
    db.refresh(db_work)
    return db_work

def get_work(db, id: int):
    return db.query(models.Work).filter(models.Work.id== id).first()

def get_work_by_status(db, status: int):
    return db.query(models.Work).filter(models.Work.status== status).all()

def work_list(db):
    return db.query(models.Work).all()

async def delete(db: Session,id: int)-> bool:
   sym1 =models.Work.__table__
   sym = sym1.delete().where(models.Work.id== id)
   print(sym)
   result = db.execute(sym)
   db.commit()
   return True