from sqlalchemy.orm import Session
from app.talent.database import SessionLocal, engine, database
from app.authentication import models
from typing import Optional
import datetime

# week1
def create_resource(db: Session,course_id:int,pdf_url:str):
    db_week = models.Resource(pdf_url=pdf_url,course_id=course_id)
    db.add(db_week)
    db.commit()
    db.refresh(db_week)
    return db_week

def get_resorce(db, id: int):
    return db.query(models.Resource).filter(models.Resource.course_id== id).first()

def get_course(db,course_id: int):
    return db.query(models.Resource).filter(models.Resource.course_id== course_id).first()

def resource_list(db):
    return db.query(models.Resource).all()

# def course_list_weekly(db,course_id:int,week:int):
#     return db.query(models.Week_Module).filter(models.Week_Module.course_id== course_id).filter(models.Week_Module.week== week).all()
