from typing import Dict, List
from fastapi import Depends,File, UploadFile, APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.authentication import models
#from courses_live.database import SessionCourse, some_engine
from app.talent.database import SessionLocal, engine,database
import shutil
import datetime
from app.utils import util
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
from . import crud, py_controller

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

models.Base.metadata.create_all(bind=engine)
 
@router.post("/course/certificate")
async def create_learn(
    client_id:str,email:str,course_id:int,lastname:str,username:str, db: Session = Depends(get_db)
):  
    userDB1 = await util.findExistedUser(username)
    if not userDB1:
        raise HTTPException(status_code =400, detail="check username")

    userDB2 = await util.findExistedEmailUser(email)
    if not userDB2:
        raise HTTPException(status_code =400, detail="check email")
    py_controller.generate_certificate_email(username,[email])
    return crud.create_certificate(db=db,email=email,lastname=lastname,username=username,course_id=course_id,client_id=client_id)

@router.put("/course/certificate/{id}")
async def update_learn(
    id:int,client_id:str,email:str,course_id:str,lastname:str,username:str, db: Session = Depends(get_db)
):
    subject =  crud.get_certificate(db,id)
    if not subject:
        raise HTTPException(status_code=404, detail="Course not found")
    query = "UPDATE certificates SET lastname='"+str(lastname)+"' ,email='"+str(email)+"' , username='"+str(username)+"', course_id = '"+str(course_id)+"' , client_id = '"+str(client_id)+"' WHERE id='"+str(id)+"'"
    db.execute(query)
    db.commit()
    return {"Result" : "Module Updated Succesfully"}

@router.get("/courses/certificate/"  ,dependencies=[Depends(pagination_params)])
def learn_list(db: Session = Depends(get_db)):
    course_all = crud.certificate_list(db=db)
    return paginate(course_all)

@router.get("/courses/certificate/{id}")
def learn_detail(id:int,db: Session = Depends(get_db)):
    course_by_id = crud.get_certificate(db=db, id=id)
    if course_by_id is None:
        raise HTTPException(status_code=404,detail="Course by this id is not in database")
    return { "Learn":course_by_id}

@router.delete("/courses/certificate/{id}")
async def delete(id: int, db: Session = Depends(get_db)):
    subject =  crud.get_certificate(db,id)
    if not subject:
        raise HTTPException(status_code=404,detail="Course by this id is not in database")
    query = "Delete From certificates WHERE id='"+str(id)+"'"
    db.execute(query)
    db.commit()
    return "deleted Succesfully"
