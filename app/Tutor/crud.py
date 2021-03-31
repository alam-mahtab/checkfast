from sqlalchemy.orm import Session
from app.talent.database import SessionLocal, engine, database
from app.authentication import models
from typing import Optional
import datetime

# week1
def create_tutor(db: Session,title:str,description:str,name:str,url:str,course_id:int,):
    db_week = models.Tutor(title=title,name=name,description=description,url=url,course_id=course_id)
    db.add(db_week)
    db.commit()
    db.refresh(db_week)
    return db_week

def get_tutor(db, id: int):
    return db.query(models.Tutor).filter(models.Tutor.id== id).first()

def get_course(db,course_id: int):
    return db.query(models.Tutor).filter(models.Tutor.course_id== course_id).first()

def tutor_list(db):
    return db.query(models.Tutor).all()

# def tutor_list_weekly(db,course_id:int,week:int):
#     return db.query(models.Tutor).filter(models.Tutor.course_id== course_id).filter(models.Tutor.week== week).all()
