# from sqlalchemy.orm import Session
# from . import schemas
# from app.talent.database import SessionLocal, engine, database
# from app.authentication import models
# from .schemas import CourseBase,CourseList
# #from datetime import datetime, timedelta
# from typing import Optional
# import datetime

# def create_comment(db:Session,courses_id:int,name:str,email:str,body:str):
#     db_comment = models.Comment(name=name,courses_id = courses_id,email=email,body=body)
#     db.add(db_comment)
#     db.commit()
#     db.refresh(db_comment)
#     return db_comment