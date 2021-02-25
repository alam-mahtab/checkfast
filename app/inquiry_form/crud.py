from sqlalchemy.orm import Session
from . import models, schemas
from .schemas import InquiryBase
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
import datetime

def create_inquiry(db: Session,title:str,name:str,desc:str,email:str,interview:bool,work_or_commision:bool,other:bool):
    db_inquiry = models.Inquiry(title=title,desc=desc,name=name,email=email,interview=interview,work_or_commision=work_or_commision,other=other)
    db.add(db_inquiry)
    db.commit()
    db.refresh(db_inquiry)
    return db_inquiry

def get_inquiry(db, id: int):
    return db.query(models.Inquiry).filter(models.Inquiry.id== id).first()

def inquiry_list(db):
    return db.query(models.Inquiry).all()
    
async def delete(db: Session,id: int)-> bool:
   sym1 =models.Inquiry.__table__
   sym = sym1.delete().where(models.Inquiry.id== id)
   print(sym)
   result = db.execute(sym)
   db.commit()
   return True