from sqlalchemy.orm import Session
from app.talent.database import SessionLocal, engine, database
from app.authentication import models
from typing import Optional
import datetime

# week1
def create_certificate(db: Session,client_id:str,course_id:int,username:str,lastname:str):
    db_week = models.Certificate(username=username,lastname=lastname,course_id=course_id,client_id=client_id)
    db.add(db_week)
    db.commit()
    db.refresh(db_week)
    return db_week

def get_certificate(db, id: int):
    return db.query(models.Certificate).filter(models.Certificate.id== id).first()

def get_course(db,course_id: int):
    return db.query(models.Certificate).filter(models.Certificate.course_id== course_id).first()

def get_user(db,client_id:str):
    return db.query(models.Certificate).filter(models.Certificate.client_id== client_id).first()

def certificate_list(db):
    return db.query(models.Certificate).all()

# def course_list_weekly(db,course_id:int,week:int):
#     return db.query(models.Week_Module).filter(models.Week_Module.course_id== course_id).filter(models.Week_Module.week== week).all()
