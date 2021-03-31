
from sqlalchemy.orm import Session
from . import models, schemas, database
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional

def create_talent(db: Session,name:str,description:str,type:str,status:int,url_profile:str, url_cover:str):
    db_talent = models.Talent(name=name,description=description,type=type,status=status,url_profile=url_profile,url_cover=url_cover)
    db.add(db_talent)
    db.commit()
    db.refresh(db_talent)
    return db_talent


def get_talent(db, id: int):
    return db.query(models.Talent).filter(models.Talent.id== id).first()

def talent_list(db):
    return db.query(models.Talent).all()

async def delete(db: Session,id: int)-> bool:
   sym1 =models.Talent.__table__
   sym = sym1.delete().where(models.Talent.id== id)
   print(sym)
   result = db.execute(sym)
   db.commit()
   return True

# 1.Writer
def writer_list(db):
    return db.query(models.Talent).filter(models.Talent.status== 1 and models.Talent.type == "Writer").all()
# 2.Director
def director_list(db):
    return db.query(models.Talent).filter(models.Talent.status== 2 and models.Talent.type == "Director").all()
# 3.Actor
def actor_list(db):
    return db.query(models.Talent).filter(models.Talent.status== 3 and models.Talent.type == "Actor").all()
# 4.Cinematographer
def cinematographer_list(db):
    return db.query(models.Talent).filter(models.Talent.status== 4 and models.Talent.type == "Cinematographer").all()
# 5.Editor
def editor_list(db):
    return db.query(models.Talent).filter(models.Talent.status== 5 and models.Talent.type == "Editor").all()
# 6.SoundEditor
def soundeditor_list(db):
    return db.query(models.Talent).filter(models.Talent.status== 6 and models.Talent.type == "SoundEditor").all()
# 7.Filmmaker
def filmmaker_list(db):
    return db.query(models.Talent).filter(models.Talent.status== 7 and models.Talent.type == "Filmmaker").all()
# 8.Videographer
def videographer_list(db):
    return db.query(models.Talent).filter(models.Talent.status== 8 and models.Talent.type == "Videographer").all()
# 9.FilmEditing
def filmediting_list(db):
    return db.query(models.Talent).filter(models.Talent.status== 9 and models.Talent.type == "FilmEditing").all()

