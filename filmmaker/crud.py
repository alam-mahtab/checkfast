
from sqlalchemy.orm import Session
from . import models, schemas
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional

def create_film_maker(db: Session,name:str,desc:str,url_profile:str, url_cover:str):
    db_film_maker = models.Filmmaker(name=name,desc=desc,url_profile=url_profile,url_cover=url_cover)
    db.add(db_film_maker)
    db.commit()
    db.refresh(db_film_maker)
    return db_film_maker


def get_film_maker(db, id: int):
    return db.query(models.Filmmaker).filter(models.Filmmaker.id== id).first()

def film_maker_list(db):
    return db.query(models.Filmmaker).all()

async def delete(db: Session,id: int)-> bool:
   sym1 =models.Filmmaker.__table__
   sym = sym1.delete().where(models.Filmmaker.id== id)
   print(sym)
   result = db.execute(sym)
   db.commit()
   return True