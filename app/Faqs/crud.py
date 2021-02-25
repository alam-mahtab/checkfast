from sqlalchemy.orm import Session
from . import models, schemas
from .schemas import InquiryBase
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
import datetime

def create_faq(db: Session,question:str,answer:str):
    db_faq = models.Question(question=question,answer=answer)
    db.add(db_faq)
    db.commit()
    db.refresh(db_faq)
    return db_faq

def get_faq(db, id: int):
    return db.query(models.Question).filter(models.Question.id== id).first()

def faq_list(db):
    return db.query(models.Question).all()
    
async def delete(db: Session,id: int)-> bool:
   sym1 =models.Question.__table__
   sym = sym1.delete().where(models.Question.id== id)
   print(sym)
   result = db.execute(sym)
   db.commit()
   return True