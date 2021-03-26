from sqlalchemy.orm import Session
from app.talent.database import SessionLocal, engine, database
#from app.authentication import models
from app.talent import models
from typing import Optional
import datetime

# Honour
def create_honour(db: Session,desc:str,name:str,url:str,talent_id:int,status:int):
    db_honour = models.Honour(desc=desc,name=name,url=url,talent_id=talent_id,status=status)
    db.add(db_honour)
    db.commit()
    db.refresh(db_honour)
    return db_honour

def get_honour(db, id: int):
    return db.query(models.Honour).filter(models.Honour.id == id).first()

def get_talent(db,talent_id: int):
    return db.query(models.Honour).filter(models.Honour.talent_id== talent_id).first()

def status_list(db):
    return db.query(models.Honour).all()

def talent_list_by_status(db,talent_id:int,status:int):
    return db.query(models.Honour).filter(models.Honour.talent_id== talent_id).filter(models.Honour.status== status).all()

# Port

def create_port(db: Session,talent_id:int,url:str,status:int):
    db_port = models.Port(url=url,status=status,talent_id=talent_id)
    db.add(db_port)
    db.commit()
    db.refresh(db_port)
    return db_port

def get_port(db, id: int):
    return db.query(models.Port).filter(models.Port.id== id).first()

def get_talents(db,talent_id: int):
    return db.query(models.Port).filter(models.Port.talent_id== talent_id).first()

def port_list(db):
    return db.query(models.Port).all()

async def delete(db: Session,id: int)-> bool:
   sym1 =models.Port.__table__
   sym = sym1.delete().where(models.Port.id== id)
   print(sym)
   result = db.execute(sym)
   db.commit()
   return True