from sqlalchemy.orm import Session
from . import schemas
from app.talent.database import SessionLocal, engine, database
from app.authentication import models
from .schemas import CourseBase,CourseList
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
import datetime

def create_course(db: Session,title:str,name:str,desc:str,price:int,url:str,type:str,status:int):
    db_course = models.Course(title=title,desc=desc,name=name,price=price,url=url,type=type,status=status)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course
# async def create_course(title:str,name:str,desc:str,price:int,url:str,type:str,status:int):
#     query = models.Course.insert().values(title=title,desc=desc,name=name,price=price,url=url,type=type,status=status)
#     return await database.execute(query)
    
# async def update_course(db: Session,id:int,title:str,name:str,desc:str,price:int,url:str,type:str,status:int):
#     db_course = models.Course.__table__.update().where(models.Course.id== id).values(title=title,desc=desc,name=name,price=price,url=url,type=type,status=status)
#     print("hello")
#     #@db.update(db_course)
#     await database.execute(db_course)
#     #db.commit()
#     print("commit")
#     # db.refresh(db_course)
#     # print("refresh")
#     return db_course
# async def update_course(db: Session,title:str,name:str,desc:str,price:int,url:str,type:str,status:int,id:int):
#     query = models.Course.__table__.update()\
#     .where(models.Course.id== id)\
#     .values(title=models.Course.title,desc=models.Course.desc,
#         name=models.Course.name,url=models.Course.url,price=models.Course.url,
#         type=models.Course.type,status=models.Course.status)
#     return await db.execute(query)

def get_course(db, id: int):
    return db.query(models.Course).filter(models.Course.id== id).first()

def course_list(db):
    return db.query(models.Course).all()

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