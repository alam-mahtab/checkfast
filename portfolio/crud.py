from sqlalchemy.orm import Session
from . import models, schemas

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional

def create_port(db: Session,url:str,status:int):
    db_port = models.Port(url=url,status=status)
    db.add(db_port)
    db.commit()
    db.refresh(db_port)
    return db_port

def get_port(db, id: int):
    return db.query(models.Port).filter(models.Port.id== id).first()

def port_list(db):
    return db.query(models.Port).all()

async def delete(db: Session,id: int)-> bool:
   sym1 =models.Port.__table__
   sym = sym1.delete().where(models.Port.id== id)
   print(sym)
   result = db.execute(sym)
   db.commit()
   return True


# Writer
def portfolio_writer_list(db):
    return db.query(models.Port).filter(models.Port.status == 1).all()
# Director
def portfolio_director_list(db):
    return db.query(models.Port).filter(models.Port.status == 2).all()
# Actor
def portfolio_actor_list(db):
    return db.query(models.Port).filter(models.Port.status == 3).all()
# Cinematographer
def portfolio_cinematographer_list(db):
    return db.query(models.Port).filter(models.Port.status == 4).all()
# Editor
def portfolio_editor_list(db):
    return db.query(models.Port).filter(models.Port.status == 5).all()
# SoundEditor
def portfolio_sound_editor_list(db):
    return db.query(models.Port).filter(models.Port.status == 6).all()
# FilmMaker
def portfolio_filmmaker_list(db):
    return db.query(models.Port).filter(models.Port.status == 7).all()
# Videographer
def portfolio_videographer_list(db):
    return db.query(models.Port).filter(models.Port.status == 8).all()
# filmEditing
def portfolio_filmediting_list(db):
    return db.query(models.Port).filter(models.Port.status == 9).all()
