
from sqlalchemy.orm import Session
from . import models, schemas
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional

def create_film_edit(db: Session,name:str,desc:str,url_profile:str, url_cover:str):
    db_film_edit = models.Filmedit(name=name,desc=desc,url_profile=url_profile,url_cover=url_cover)
    db.add(db_film_edit)
    db.commit()
    db.refresh(db_film_edit)
    return db_film_edit


def get_film_edit(db, id: int):
    return db.query(models.Filmedit).filter(models.Filmedit.id== id).first()

def film_edit_list(db):
    return db.query(models.Filmedit).all()

async def delete(db: Session,id: int)-> bool:
   sym1 =models.Filmedit.__table__
   sym = sym1.delete().where(models.Filmedit.id== id)
   print(sym)
   result = db.execute(sym)
   db.commit()
   return True