from sqlalchemy.orm import Session
from app.talent.database import SessionLocal, engine, database
from app.authentication import models
from typing import Optional
import datetime

# week1
def create_week(db: Session,title:str,name:str,url:str,course_id:int,week:int):
    db_week = models.Week_Module(title=title,name=name,url=url,course_id=course_id,week=week)
    db.add(db_week)
    db.commit()
    db.refresh(db_week)
    return db_week

def get_week(db, id: int):
    return db.query(models.Week_Module).filter(models.Week_Module.id== id).first()

def get_course(db,course_id: int):
    return db.query(models.Week_Module).filter(models.Week_Module.course_id== course_id).first()

def week_list(db):
    return db.query(models.Week_Module).all()

def course_list_weekly(db,course_id:int,week:int):
    return db.query(models.Week_Module).filter(models.Week_Module.course_id== course_id).filter(models.Week_Module.week== week).all()
