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
 
@router.post("/course/tutor")
def create_tutor(
    course_id:int,title:str,name:str,description:str,file: UploadFile= File(...), db: Session = Depends(get_db)
):

    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not extension:
        return "Image must be jpg or png format!"
    result = cloudinary.uploader.upload(file.file)
    url = result.get("url")
    return crud.create_tutor(db=db,name=name,title=title,description=description,url=url,course_id=course_id)

@router.put("/course/tutor/{id}")
async def update_tutor(
    id:int,course_id:int,title:str,name:str,description:str,file: UploadFile= File(...), db: Session = Depends(get_db)
):
    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not extension:
        return "Image must be jpg or png format!"
    result = cloudinary.uploader.upload(file.file)
    url = result.get("url")
    subject =  crud.get_tutor(db,id)
    if not subject:
        raise HTTPException(status_code=404, detail="Course not found")
    #'select * from USERS where email='+"'"+str(username)+"'"+' and PASSWORD='+"'"+str(password)+"'"
    query = "UPDATE tutors SET title='"+str(title)+"' , name='"+str(name)+"' , description='"+str(description)+"', COURSE_ID = '"+str(course_id)+"' , url='"+str(url)+"' WHERE id='"+str(id)+"'"
    db.execute(query)
    db.commit()
    return {"Result" : "Module Updated Succesfully"}

@router.get("/courses/tutor/"  ,dependencies=[Depends(pagination_params)])
def tutor_list(db: Session = Depends(get_db)):
    course_all = crud.tutor_list(db=db)
    return paginate(course_all)

@router.get("/courses/tutor/{id}")
def tutor_detail(id:int,db: Session = Depends(get_db)):
    course_by_id = crud.get_tutor(db=db, id=id)
    if course_by_id is None:
        raise HTTPException(status_code=404,detail="Course by this id is not in database")
    return { "Tutor":course_by_id}

@router.delete("/courses/tutor/{id}")
async def delete(id: int, db: Session = Depends(get_db)):
    subject =  crud.get_tutor(db,id)
    if not subject:
        raise HTTPException(status_code=404,detail="Course by this id is not in database")
    query = "Delete From tutors WHERE id='"+str(id)+"'"
    db.execute(query)
    db.commit()
    return "deleted Succesfully"
