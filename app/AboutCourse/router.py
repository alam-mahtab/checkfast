from typing import Dict, List
from fastapi import Depends,File, UploadFile, APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.authentication import models
#from courses_live.database import SessionCourse, some_engine
from app.talent.database import SessionLocal, engine,database
import shutil
import datetime
#from coursebysubject.models import subjects
# Pagination
from fastapi_pagination import Page, pagination_params
from fastapi_pagination.paginator import paginate
router = APIRouter()


import uuid
from pathlib import Path
import time
#from fastapi.staticfiles import StaticFiles
from starlette.staticfiles import StaticFiles
import os
from os.path import dirname, abspath, join
import cloudinary
import cloudinary.uploader
from . import crud

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

models.Base.metadata.create_all(bind=engine)
 
@router.post("/course/about")
def create_about(
    course_id:int,heading:str,desc:str,title:str,name:str, db: Session = Depends(get_db)
):
    return crud.create_week(db=db,name=name,title=title,heading=heading,desc=desc,course_id=course_id)

@router.put("/course/about/{id}")
async def update_about(
    id:int,course_id:int,heading:str,desc:str,title:str,name:str, db: Session = Depends(get_db)
):
    query = "UPDATE aboutcourses SET title='"+str(title)+"' , name='"+str(name)+"', COURSE_ID = '"+str(course_id)+"'  , heading='"+str(heading)+"', desc='"+str(desc)+"' WHERE id='"+str(id)+"'"
    db.execute(query)
    db.commit()
    return {"Result" : "Module Updated Succesfully"}

@router.get("/courses/about/"  ,dependencies=[Depends(pagination_params)])
def about_list(db: Session = Depends(get_db)):
    course_all = crud.about_list(db=db)
    return paginate(course_all)

@router.get("/courses/about/{id}")
def about_detail(id:int,db: Session = Depends(get_db)):
    course_by_id = crud.get_About(db=db, id=id)
    if course_by_id is None:
        raise HTTPException(status_code=404,detail="About by this id is not in database")
    return { "About":course_by_id}

@router.delete("/courses/about/{id}")
async def delete(id: int, db: Session = Depends(get_db)):
    subject =  crud.get_About(db,id)
    if not subject:
        raise HTTPException(status_code=404,detail="Course by this id is not in database")
    query = "Delete From aboutcourses WHERE id='"+str(id)+"'"
    db.execute(query)
    db.commit()
    return "deleted Succesfully"
