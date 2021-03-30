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
 
@router.post("/course/learn")
def create_learn(
    course_id:int,text1:str,text2:str,text3:str,text4:str, db: Session = Depends(get_db)
):
    return crud.create_week(db=db,text1=text1,text2=text2,text3=text3,text4=text4,course_id=course_id)

@router.put("/course/learn/{id}")
async def update_learn(
    id:int,course_id:int,text1:str,text2:str,text3:str,text4:str, db: Session = Depends(get_db)
):
    subject =  crud.get_learn(db,id)
    if not subject:
        raise HTTPException(status_code=404, detail="Course not found")
    query = "UPDATE weeks SET text1='"+str(text1)+"' , text2='"+str(text2)+"', text3 = '"+str(text3)+"'  , text4='"+str(text4)+"' WHERE id='"+str(id)+"'"
    db.execute(query)
    db.commit()
    return {"Result" : "Module Updated Succesfully"}

@router.get("/courses/learn/"  ,dependencies=[Depends(pagination_params)])
def learn_list(db: Session = Depends(get_db)):
    course_all = crud.learn_list(db=db)
    return paginate(course_all)

@router.get("/courses/learn/{id}")
def learn_detail(id:int,db: Session = Depends(get_db)):
    course_by_id = crud.get_learn(db=db, id=id)
    if course_by_id is None:
        raise HTTPException(status_code=404,detail="Course by this id is not in database")
    return { "Learn":course_by_id}

@router.delete("/courses/learn/{id}")
async def delete(id: int, db: Session = Depends(get_db)):
    subject =  crud.get_learn(db,id)
    if not subject:
        raise HTTPException(status_code=404,detail="Course by this id is not in database")
    query = "Delete From learns WHERE id='"+str(id)+"'"
    db.execute(query)
    db.commit()
    return "deleted Succesfully"
