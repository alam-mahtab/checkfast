from sqlalchemy.orm import Session
from . import schemas
from app.talent.database import SessionLocal, engine, database
from app.authentication import models
from .schemas import CourseBase,CourseList
#from datetime import datetime, timedelta
from typing import Optional
import datetime

def create_course(db: Session,title:str,name:str,description:str,price:int,url:str,type:str,status:int,short_desc:str,module:str):
    db_course = models.Course(title=title,description=description,name=name,price=price,url=url,type=type,status=status,short_desc=short_desc,module=module)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course
    
def create_comment(db:Session,courses_id:int,name:str,Message:str):
    db_comment = models.Comment(name=name,courses_id = courses_id,Message=Message)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def get_course(db, id: int):
    return db.query(models.Course).filter(models.Course.id== id).first()
def course_list(db):
    return db.query(models.Course).all()

def get_comment(db, id: int):
    return db.query(models.Comment).filter(models.Comment.courses_id== id).all()
def comment_list(db):
    return db.query(models.Comment).all()

# Wishlist
def create_wishlist(db:Session,course_id:int,client_id:str):
    db_wish = models.Wishlist(course_id = course_id,client_id=client_id)
    db.add(db_wish)
    db.commit()
    db.refresh(db_wish)
    return db_wish

def get_wishlist(db, id: int):
    return db.query(models.Wishlist).filter(models.Wishlist.client_id== id).all()
def get_wishlist_course_id(db, id: int):
    return db.query(models.Wishlist.course_id).filter(models.Wishlist.client_id== id).all()
def get_wishlist_course_by_id(db, id: int):
    return db.query(models.Course).filter(models.Course.id== id).all()
def wishlist_list(db):
    return db.query(models.Wishlist).all()

async def delete_wishlist(db: Session,id: int)-> bool:
   sym1 =models.Wishlist.__table__
   sym = sym1.delete().where(models.Wishlist.id== id)
   print(sym)
   result = db.execute(sym)
   db.commit()
   return True

# Project Undertaken
def create_project(db:Session,client_id:str,url:str,first_name:str,details:str):
    db_wish = models.Project(client_id=client_id,url=url,first_name=first_name,details=details)
    db.add(db_wish)
    db.commit()
    db.refresh(db_wish)
    return db_wish

def get_project(db, id: int):
    return db.query(models.Project).filter(models.Project.client_id== id).all()
def get_project_course_id(db, id: int):
    return db.query(models.Project.course_id).filter(models.Project.client_id== id).all()
def project_list(db):
    return db.query(models.Project).all()

async def delete_project(db: Session,id: int)-> bool:
   sym1 =models.Project.__table__
   sym = sym1.delete().where(models.Project.id== id)
   print(sym)
   result = db.execute(sym)
   db.commit()
   return True

# Notes
def create_notes(db:Session,client_id:str,detail:str):
    db_wish = models.Notes(client_id=client_id,detail=detail)
    db.add(db_wish)
    db.commit()
    db.refresh(db_wish)
    return db_wish

def get_notes(db, client_id: int):
    return db.query(models.Notes).filter(models.Notes.client_id== client_id).all()
def get_notes_course_id(db, id: int):
    return db.query(models.Notes.course_id).filter(models.Notes.client_id== id).all()
def notes_list(db):
    return db.query(models.Notes).all()

async def delete_notes(db: Session,id: int)-> bool:
   sym1 =models.Notes.__table__
   sym = sym1.delete().where(models.Notes.id== id)
   print(sym)
   result = db.execute(sym)
   db.commit()
   return True


def master_list(db):
    return db.query(models.Course).filter(models.Course.status== 1 and models.Course.type == "Master").all()

def extensive_list(db):
    return db.query(models.Course).filter(models.Course.status== 2 and models.Course.type == "Extensive").all()

def micro_list(db):
    return db.query(models.Course).filter(models.Course.status== 3 and models.Course.type == "Micro").all()

def live_list(db):
    return db.query(models.Course).filter(models.Course.status== 4 and models.Course.type == "Live").all()

def profession_list(db):
    return db.query(models.Course).filter(models.Course.status== 5 and models.Course.type == "Profession").all()

def subject_list(db):
    return db.query(models.Course).filter(models.Course.status== 6 and models.Course.type == "Subject").all()

def free_list(db):
    return db.query(models.Course).filter(models.Course.status== 7 and models.Course.type == "Free").all()   
async def delete(db: Session,id: int)-> bool:
   sym1 =models.Course.__table__
   sym = sym1.delete().where(models.Course.id== id)
   print(sym)
   result = db.execute(sym)
   db.commit()
   return True

# # async def update_subject(db: Session,title:str,name:str,desc:str,url:str,subject_id:int):
# #     query = models.Subject.__table__.update()\
# #     .where(models.Subject.id== subject_id)\
# #     .values(title=title,desc=desc,name=name,url=url).returning(models.Subject.id)
# #     #db_subjects = models.Subject(title=title,desc=desc,name=name,url=url)
# #     # db.execute(db_subj)
# #     # db.commit()
# #     # db.refresh(db_subj)
# #     # return db_subj
# #     #return db.execute(query)
# #     return True

# async def update_subject(db: Session,
# #title:str,name:str,desc:str,url:str,id=int,
#  subject = schemas.SubjectBase):
#     db_subject = db.query(models.Subject).filter(models.Subject.id == id).first()
#     db_subject.title = subject.title
#     db_subject.name = subject.name
#     #db_subject.url = models.Subject.__table__.url
#     db_subject.desc = subject.desc
#     db.commit()
#     db.refresh(db_subject)
#     return await db_subject
# # async def update_subject(db: Session,id: int, payload: SubjectUpdate):
# #     query = (
# #         models.Subject.__table__
# #         .update()
# #         .where(id == models.Subject.id)
# #         .values(name=payload.name,title=payload.title,description=payload.desc)
# #         .returning(models.Subject.id)
# #     )
# #     return await db.execute(query=query)
   
# # async def put_sub(db: Session, id: int, subj :schemas.SubjectUpdate):
# #     gdate = str(datetime.datetime.now())
# #     query = models.Subject.__table__.update().\
# #         where(models.Subject.id == id).\
# #         values(
# #         name = models.Subject.name,
# #         title = models.Subject.title,
# #         desc = models.Subject.desc,
# #         #password = util.get_password_hash(user.password),#
# #         #confirm_password =  util.get_password_hash(user.confirm_password),#
# #         # first_name = user.first_name,
# #         # last_name = user.last_name,
# #         # dateofbirth = user.dateofbirth,
# #         # phone = user.phone,
# #         created_date = gdate,
# #         )
# #     db.execute(query)
# #     db.commit()
# #     return True