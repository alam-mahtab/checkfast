from sqlalchemy.orm import Session
from app.talent.database import SessionLocal, engine, database
from app.authentication import models
from typing import Optional
import datetime

# week1
def create_About(db: Session,heading:str,description:str,title:str,name:str,course_id:int):
    db_About = models.AboutCourse(title=title,name=name,heading=heading,course_id=course_id,description=description)
    db.add(db_About)
    db.commit()
    db.refresh(db_About)
    return db_About

def get_About(db, id: int):
    return db.query(models.AboutCourse).filter(models.AboutCourse.id== id).first()

def get_course(db,course_id: int):
    return db.query(models.AboutCourse).filter(models.AboutCourse.course_id== course_id).first()

def about_list(db):
    return db.query(models.AboutCourse).all()

# def course_list_weekly(db,course_id:int,week:int):
#     return db.query(models.AboutCourse).filter(models.AboutCourse.course_id== course_id).filter(models.Week_Module.week== week).all()
