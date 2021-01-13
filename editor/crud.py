
from sqlalchemy.orm import Session
from . import models, schemas
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional

def create_editor(db: Session,name:str,desc:str,url_profile:str, url_cover:str):
    db_editor = models.Editor(name=name,desc=desc,url_profile=url_profile,url_cover=url_cover)
    db.add(db_editor)
    db.commit()
    db.refresh(db_editor)
    return db_editor


def get_editor(db, id: int):
    return db.query(models.Editor).filter(models.Editor.id== id).first()

def editor_list(db):
    return db.query(models.Editor).all()

async def delete(db: Session,id: int)-> bool:
   sym1 =models.Editor.__table__
   sym = sym1.delete().where(models.Editor.id== id)
   print(sym)
   result = db.execute(sym)
   db.commit()
   return True