from sqlalchemy.orm import Session
from app.talent.database import SessionLocal, engine, database
from app.authentication import models
from typing import Optional
import datetime

# week1
def create_learn(db: Session,course_id:int,text1:str,text2:str,text3:str,text4:str):
    db_week = models.Learn(text1=text1,text2=text2,text3=text3,text4=text4,course_id=course_id)
    db.add(db_week)
    db.commit()
    db.refresh(db_week)
    return db_week

def get_learn(db, id: int):
    return db.query(models.Learn).filter(models.Learn.id== id).first()

def get_course(db,course_id: int):
    return db.query(models.Learn).filter(models.Learn.course_id== course_id).first()

def learn_list(db):
    return db.query(models.Learn).all()

# def course_list_weekly(db,course_id:int,week:int):
#     return db.query(models.Week_Module).filter(models.Week_Module.course_id== course_id).filter(models.Week_Module.week== week).all()
