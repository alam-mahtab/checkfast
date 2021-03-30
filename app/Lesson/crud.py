from sqlalchemy.orm import Session
from app.talent.database import SessionLocal, engine, database
from app.authentication import models
from typing import Optional
import datetime

# week1
def create_lesson(db: Session,title:str,name:str,description:str,url:str,course_id:int,chapter:int):
    db_week = models.Lesson(title=title,name=name,description=description,url=url,course_id=course_id,chapter=chapter)
    db.add(db_week)
    db.commit()
    db.refresh(db_week)
    return db_week

def get_lesson(db, id: int):
    return db.query(models.Lesson).filter(models.Lesson.id== id).first()

def get_course(db,course_id: int):
    return db.query(models.Lesson).filter(models.Lesson.course_id== course_id).first()

def lesson_list(db):
    return db.query(models.Lesson).all()

def course_list_weekly(db,course_id:int,chapter:int):
    return db.query(models.Lesson).filter(models.Lesson.course_id== course_id).filter(models.Lesson.chapter== chapter).all()
