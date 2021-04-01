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
 
@router.post("/course/resource")
def create_learn(
    course_id:int,file: UploadFile= File(...), db: Session = Depends(get_db)
):  
    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")#("pdf", "txt", "docs")
    if not extension:
        return "Documents must be pdf or txt format!"
    
    # outputImage = Image.fromarray(sr_img)  
    suffix = Path(file.filename).suffix
    filename = time.strftime( str(uuid.uuid4().hex) + "%Y%m%d-%H%M%S" + suffix )
    result = cloudinary.uploader.upload(file.file)
    pdf_url = result.get("url")
    return crud.create_resource(db=db,pdf_url=pdf_url,course_id=course_id)

@router.put("/course/resource/{id}")
async def update_learn(
    id:int,course_id:int,file: UploadFile= File(...), db: Session = Depends(get_db)
):  
    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not extension:
        return "Documents must be pdf or txt format!"
    
    # outputImage = Image.fromarray(sr_img)  
    suffix = Path(file.filename).suffix
    filename = time.strftime( str(uuid.uuid4().hex) + "%Y%m%d-%H%M%S" + suffix )
    result = cloudinary.uploader.upload(file.file)
    pdf_url = result.get("url")
    subject =  crud.get_resorce(db,id)
    if not subject:
        raise HTTPException(status_code=404, detail="Course not found")
    query = "UPDATE resources SET course_id='"+str(course_id)+"' , pdf_url='"+str(pdf_url)+"' WHERE id='"+str(id)+"'"
    db.execute(query)
    db.commit()
    return {"Result" : "Module Updated Succesfully"}

@router.get("/courses/resource/"  ,dependencies=[Depends(pagination_params)])
def learn_list(db: Session = Depends(get_db)):
    course_all = crud.resource_list(db=db)
    return paginate(course_all)

@router.get("/courses/resource/{id}")
def learn_detail(id:int,db: Session = Depends(get_db)):
    course_by_id = crud.get_resorce(db=db, id=id)
    if course_by_id is None:
        raise HTTPException(status_code=404,detail="Course by this id is not in database")
    return { "Learn":course_by_id}

@router.delete("/courses/resource/{id}")
async def delete(id: int, db: Session = Depends(get_db)):
    subject =  crud.get_resorce(db,id)
    if not subject:
        raise HTTPException(status_code=404,detail="Course by this id is not in database")
    query = "Delete From resources WHERE id='"+str(id)+"'"
    db.execute(query)
    db.commit()
    return "deleted Succesfully"
