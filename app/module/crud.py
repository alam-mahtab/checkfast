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
    # query = " Select * From weeks where course_id='"+str(course_id)+"' and week='"+str(week)+"'"
    # #return db.query(" Select * From weeks where course_id='"+str(course_id)+"' and week='"+str(week)+"'")
    # db_ad = db.execute(query)
    # db.commit()
    # db.refresh(query)
    # print(query)
    # return query


# def course_list_weekly(db, course_id:int, id:int):
#     db_week= "select * From weeks where course_id='"+str(course_id)+"' And week='"+str(id)+"'"
#     db.execute(db_week)
#     db.commit()
#     db.refresh(db_week)
#     return db_week

# async def delete_week(db: Session,id: int):
# #    sym1 =models.Week_Module.__table__.delete().where(models.Week_Module.id== id)
# #    result1 = db.execute(sym1)
# #    print(result1, "result1")
# #    result2 =db.commit()
# #    print(result2, "result2")
# #    return True
#     query = "Delete From weeks WHERE id='"+str(id)+"'"
#     return db.query()