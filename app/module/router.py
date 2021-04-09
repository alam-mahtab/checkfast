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
from s3_events.s3_utils import S3_SERVICE
from app.configs import bucketinfo
def bucket_config():
    return bucketinfo.setting()


AWS_ACCESS_KEY_ID =  bucket_config().AWS_ACCESS_KEY_ID#os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY =  bucket_config().AWS_SECRET_ACCESS_KEY#os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION =  bucket_config().AWS_REGION #os.getenv("AWS_REGION")
S3_Bucket = bucket_config().S3_Bucket #os.getenv("S3_Bucket")
S3_Key = "module" # change everywhere
PUBLIC_DESTINATION = "https://cinedarbaar.s3.ap-south-1.amazonaws.com/"
s3_client = S3_SERVICE(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION)
 
@router.post("/course/week")
async def create_course(
    course_id:int,title:str,name:str,week:int,fileobject: UploadFile= File(...), filename: str = Body(default=None), db: Session = Depends(get_db)
):

    if filename is None:
        #filename = generate_png_string()
        extension_pro = fileobject.filename.split(".")[-1] in ("jpg", "jpeg", "png") 
        if not extension_pro:
            return "Image must be jpg or png format!"
        suffix_pro = Path(fileobject.filename).suffix
        filename = time.strftime( str(uuid.uuid4().hex) + "%Y%m%d-%H%M%S" + suffix_pro )
    data = fileobject.file._file  # Converting tempfile.SpooledTemporaryFile to io.BytesIO
    uploads3 = await s3_client.upload_fileobj(bucket=S3_Bucket, key=S3_Key+"/"+filename, fileobject=data )
    if uploads3:
        url = os.path.join(PUBLIC_DESTINATION, S3_Key+"/"+filename)
        return crud.create_week(db=db,name=name,title=title,url=url,course_id=course_id,week=week)
    else:
        raise HTTPException(status_code=400, detail="Failed to upload in S3")

@router.put("/course/week/{id}")
async def update_course(
    id:int,course_id:int,title:str,name:str,week:int,fileobject: UploadFile= File(...), filename: str = Body(default=None), db: Session = Depends(get_db)
):
    if filename is None:
        #filename = generate_png_string()
        extension_pro = fileobject.filename.split(".")[-1] in ("jpg", "jpeg", "png") 
        if not extension_pro:
            return "Image must be jpg or png format!"
        suffix_pro = Path(fileobject.filename).suffix
        filename = time.strftime( str(uuid.uuid4().hex) + "%Y%m%d-%H%M%S" + suffix_pro )
    data = fileobject.file._file  # Converting tempfile.SpooledTemporaryFile to io.BytesIO
    uploads3 = await s3_client.upload_fileobj(bucket=S3_Bucket, key=S3_Key+"/"+filename, fileobject=data )
    if uploads3:
        url = os.path.join(PUBLIC_DESTINATION, S3_Key+"/"+filename)
        subject =  crud.get_week(db,id)
        if not subject:
            raise HTTPException(status_code=404, detail="Course not found")
        #'select * from USERS where email='+"'"+str(username)+"'"+' and PASSWORD='+"'"+str(password)+"'"
        query = "UPDATE weeks SET title='"+str(title)+"' , name='"+str(name)+"', COURSE_ID = '"+str(course_id)+"'  , week='"+str(week)+"', url='"+str(url)+"' WHERE id='"+str(id)+"'"
        db.execute(query)
        db.commit()
        return {"Result" : "Module Updated Succesfully"}
    else:
        raise HTTPException(status_code=400, detail="Failed to upload in S3")

@router.get("/courses/week/"  ,dependencies=[Depends(pagination_params)])
def course_list(db: Session = Depends(get_db)):
    course_all = crud.week_list(db=db)
    return paginate(course_all)

@router.get("/courses/week/{id}")
def course_detail(id:int,db: Session = Depends(get_db)):
    course_by_id = crud.get_week(db=db, id=id)
    if course_by_id is None:
        raise HTTPException(status_code=404,detail="Course by this id is not in database")
    return { "course":course_by_id}

@router.get("/courses/week_wise/{course_id}/{week}")
def course_detail_weekly(course_id:int,week:int,db: Session = Depends(get_db)):
    course_week = crud.course_list_weekly(db, course_id, week)
    if not course_week:
        raise HTTPException(status_code=404,detail="Course by this id is not in database")
    return { "course":course_week}

@router.delete("/courses/week/{id}")
async def delete(id: int, db: Session = Depends(get_db)):
    subject =  crud.get_week(db,id)
    if not subject:
        raise HTTPException(status_code=404,detail="Course by this id is not in database")
    query = "Delete From weeks WHERE id='"+str(id)+"'"
    db.execute(query)
    db.commit()
    return "deleted Succesfully"
