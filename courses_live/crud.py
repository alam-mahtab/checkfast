
from sqlalchemy.orm import Session
from . import models, schemas, database
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional

def create_live(db: Session,title:str,name:str,desc:str,url:str):
    db_live = models.Live(title=title,desc=desc,name=name,url=url)
    db.add(db_live)
    db.commit()
    db.refresh(db_live)
    return db_live

# def update_live(db, id:int, title:str,name:str,desc:str,url:str):
#     query = models.Live.__table__.update(models.live.title == title).where(models.Live.id== id)
#     db.commit()
    
#     return True

def get_live(db, id: int):
    return db.query(models.Live).filter(models.Live.id== id).first()

def live_list(db):
    return db.query(models.Live).all()

async def delete(db: Session,id: int)-> bool:
   sym1 =models.Live.__table__
   sym = sym1.delete().where(models.Live.id== id)
   print(sym)
   result = db.execute(sym)
   db.commit()
   return True