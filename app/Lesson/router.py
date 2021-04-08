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

import boto3
from fastapi.param_functions import File, Body
from s3_events.s3_utils import S3_SERVICE_VIDEO
AWS_ACCESS_KEY_ID = "AKIA2O3WJVIG42BHMUPF"
AWS_SECRET_ACCESS_KEY = "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"
S3_Key = "lesson" # change everywhere
S3_Bucket = 'cinedarbaar'
AWS_REGION = 'ap-south-1'
DESTINATION = "static/"
PUBLIC_DESTINATION = "https://cinedarbaar.s3.ap-south-1.amazonaws.com/"
s3_client = S3_SERVICE_VIDEO(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION)
 
@router.post("/course/lesson")
async def create_lesson(
    course_id:int,title:str,name:str,description:str,chapter:int,fileobject: UploadFile= File(...), filename: str = Body(default=None), db: Session = Depends(get_db)
):

    if filename is None:
        #filename = generate_png_string()
        extension_pro = fileobject.filename.split(".")[-1] in ("mp4", "3gp", "mkv") 
        if not extension_pro:
            return "video must be jpg or png format!"
        suffix_pro = Path(fileobject.filename).suffix
        filename = time.strftime( str(uuid.uuid4().hex) + "%Y%m%d-%H%M%S" + suffix_pro )
    data = fileobject.file._file  # Converting tempfile.SpooledTemporaryFile to io.BytesIO
    uploads3 = await s3_client.upload_fileobj(bucket=S3_Bucket, key=S3_Key+"/"+filename, fileobject=data)
    if uploads3:
        url = os.path.join(PUBLIC_DESTINATION, S3_Key+"/"+filename)
        return crud.create_lesson(db=db,name=name,title=title,description=description,url=url,course_id=course_id,chapter=chapter)
    else:
        raise HTTPException(status_code=400, detail="Failed to upload in S3")

@router.put("/course/lesson/{id}")
async def update_lesson(
    id:int,course_id:int,title:str,name:str,description:str,chapter:int,fileobject: UploadFile= File(...), filename: str = Body(default=None), db: Session = Depends(get_db)
):
    if filename is None:
        #filename = generate_png_string()
        extension_pro = fileobject.filename.split(".")[-1] in ("mp4", "3gp", "mkv") 
        if not extension_pro:
            return "video must be jpg or png format!"
        suffix_pro = Path(fileobject.filename).suffix
        filename = time.strftime( str(uuid.uuid4().hex) + "%Y%m%d-%H%M%S" + suffix_pro )
    data = fileobject.file._file  # Converting tempfile.SpooledTemporaryFile to io.BytesIO
    uploads3 = await s3_client.upload_fileobj(bucket=S3_Bucket, key=S3_Key+"/"+filename, fileobject=data )
    if uploads3:
        url = os.path.join(PUBLIC_DESTINATION, S3_Key+"/"+filename)
        subject =  crud.get_lesson(db,id)
        if not subject:
            raise HTTPException(status_code=404, detail="Lesson not found")
        query = "UPDATE lessons SET title='"+str(title)+"' , name='"+str(name)+"', description ='"+str(description)+"', COURSE_ID = '"+str(course_id)+"'  , chapter='"+str(chapter)+"', url='"+str(url)+"' WHERE id='"+str(id)+"'"
        db.execute(query)
        db.commit()
        return {"Result" : "Module Updated Succesfully"}
    else:
        raise HTTPException(status_code=400, detail="Failed to upload in S3")

@router.get("/courses/lesson/"  ,dependencies=[Depends(pagination_params)])
def lesson_list(db: Session = Depends(get_db)):
    course_all = crud.lesson_list(db=db)
    return paginate(course_all)

@router.get("/courses/lesson/{id}")
def course_detail(id:int,db: Session = Depends(get_db)):
    course_by_id = crud.get_lesson(db=db, id=id)
    if course_by_id is None:
        raise HTTPException(status_code=404,detail="Course by this id is not in database")
    return { "Lesson":course_by_id}

@router.get("/courses/lesson/{course_id}/{chapter}")
def course_detail_weekly(course_id:int,chapter:int,db: Session = Depends(get_db)):
    course_week = crud.course_list_weekly(db, course_id, chapter)
    if not course_week:
        raise HTTPException(status_code=404,detail="Course by this id is not in database")
    return { "Lesson":course_week}

@router.delete("/courses/lesson/{id}")
async def delete(id: int, db: Session = Depends(get_db)):
    subject =  crud.get_lesson(db,id)
    if not subject:
        raise HTTPException(status_code=404,detail="Course by this id is not in database")
    query = "Delete From lessons WHERE id='"+str(id)+"'"
    db.execute(query)
    db.commit()
    return "deleted Succesfully"
