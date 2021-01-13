
from sqlalchemy.orm import Session
from . import models, schemas
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional

def create_actor(db: Session,name:str,desc:str,url_profile:str, url_cover:str):
    db_actor = models.Actor(name=name,desc=desc,url_profile=url_profile,url_cover=url_cover)
    db.add(db_actor)
    db.commit()
    db.refresh(db_actor)
    return db_actor


def get_actor(db, id: int):
    return db.query(models.Actor).filter(models.Actor.id== id).first()

def actor_list(db):
    return db.query(models.Actor).all()

async def delete(db: Session,id: int)-> bool:
   sym1 =models.Actor.__table__
   sym = sym1.delete().where(models.Actor.id== id)
   print(sym)
   result = db.execute(sym)
   db.commit()
   return True