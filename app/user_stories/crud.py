from sqlalchemy.orm import Session
from . import models, schemas

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional

def create_story(db: Session,url:str,story:str):
    db_story = models.Story(url=url,story=story)
    db.add(db_story)
    db.commit()
    db.refresh(db_story)
    return db_story

def get_story(db, id: int):
    return db.query(models.Story).filter(models.Story.id== id).first()

def story_list(db):
    return db.query(models.Story).all()

async def delete(db: Session,id: int)-> bool:
   sym1 =models.Story.__table__
   sym = sym1.delete().where(models.Story.id== id)
   print(sym)
   result = db.execute(sym)
   db.commit()
   return True