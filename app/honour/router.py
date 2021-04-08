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
# For S3
from fastapi.param_functions import File, Body
from s3_events.s3_utils import S3_SERVICE
AWS_ACCESS_KEY_ID = "AKIA2O3WJVIG42BHMUPF"
AWS_SECRET_ACCESS_KEY = "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"
S3_Key = "honour" # change everywhere
S3_Bucket = 'cinedarbaar'
AWS_REGION = 'ap-south-1'
DESTINATION = "static/"
PUBLIC_DESTINATION = "https://cinedarbaar.s3.ap-south-1.amazonaws.com/"
s3_client = S3_SERVICE(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION)
 
@router.post("/talent/honour")
async def create_honour(
    talent_id:int,description:str,name:str,status:int,fileobject: UploadFile= File(...), filename: str = Body(default=None), db: Session = Depends(get_db)
):

    if filename is None:
        #filename = generate_png_string()
        extension_pro = fileobject.filename.split(".")[-1] in ("jpg", "jpeg", "png") 
        if not extension_pro:
            return "Image must be jpg or png format!"
        suffix_pro = Path(fileobject.filename).suffix
        filename = time.strftime( str(uuid.uuid4().hex) + "%Y%m%d-%H%M%S" + suffix_pro )
    data = fileobject.file._file  # Converting tempfile.SpooledTemporaryFile to io.BytesIO
    uploads3 = await s3_client.upload_fileobj(bucket=S3_Bucket, key=S3_Key+"/"+filename, fileobject=data)
    if uploads3:
        url = os.path.join(PUBLIC_DESTINATION, S3_Key+"/"+filename)
        return crud.create_honour(db=db,talent_id=talent_id,name=name,url=url,description=description,status=status)
    else:
        raise HTTPException(status_code=400, detail="Failed to upload in S3")

@router.put("/talent/honour/{id}")
async def update_talent(
    id:int,talent_id:int,description:str,name:str,status:int,fileobject: UploadFile= File(...), filename: str = Body(default=None), db: Session = Depends(get_db)
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
        subject =  crud.get_honour(db,id)
        if not subject:
            raise HTTPException(status_code=404, detail="Module not found")
        #'select * from USERS where email='+"'"+str(username)+"'"+' and PASSWORD='+"'"+str(password)+"'"
        query = "UPDATE honours SET description='"+str(description)+"' , name='"+str(name)+"', talent_id = '"+str(talent_id)+"'  , status='"+str(status)+"', url='"+str(url)+"' WHERE id='"+str(id)+"'"
        db.execute(query)
        db.commit()
        return {"Result" : "Module Updated Succesfully"}
    else:
        raise HTTPException(status_code=400, detail="Failed to upload in S3")

@router.get("/talent/honour"  ,dependencies=[Depends(pagination_params)])
def talent_list(db: Session = Depends(get_db)):
    course_all = crud.status_list(db=db)
    return paginate(course_all)

@router.get("/talent/honour/{id}")
def talent_detail(id:int,db: Session = Depends(get_db)):
    course_by_id = crud.get_honour(db=db, id=id)
    if course_by_id is None:
        raise HTTPException(status_code=404,detail="Course by this id is not in database")
    return { "course":course_by_id}

@router.get("/talent/honour/{talent_id}/{status}")
def talent_detail_status_wise(talent_id:int,status:int,db: Session = Depends(get_db)):
    course_week = crud.talent_list_by_status(db, talent_id, status)
    if not course_week:
        raise HTTPException(status_code=404,detail="Talent by this id is not in database")
    return { "Talent":course_week}

@router.delete("/talent/honour/{id}")
async def delete(id: int, db: Session = Depends(get_db)):
    subject =  crud.get_honour(db,id)
    if not subject:
        raise HTTPException(status_code=404,detail="Talent by this id is not in database")
    query = "Delete From honours WHERE id='"+str(id)+"'"
    db.execute(query)
    db.commit()
    return "deleted Succesfully"

# PORT
@router.post("/talent/port")
def create_port(
    talent_id:int,url:str,status:int, db: Session = Depends(get_db)
):
    return crud.create_port(db=db,url=url,talent_id=talent_id,status=status)

@router.put("/talent/port/{id}")
async def update_port(
    id:int,talent_id:int,url:str,db: Session = Depends(get_db)
):
    subject =  crud.get_port(db,id)
    if not subject:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    #'select * from USERS where email='+"'"+str(username)+"'"+' and PASSWORD='+"'"+str(password)+"'"
    query = "UPDATE ports SET talent_id = '"+str(talent_id)+"' , url='"+str(url)+"' WHERE id='"+str(id)+"'"
    db.execute(query)
    db.commit()
    return {"Result" : "Portfolio Updated Succesfully"}
#     return await crud.update_course(db=db,name=name,title=title,desc=desc,price=price,url=url,type=type,status=status)
#     #return {"update": update}

@router.get("/talent/port"  ,dependencies=[Depends(pagination_params)])
def port_list(db: Session = Depends(get_db)):
    course_all = crud.port_list(db=db)
    return paginate(course_all)

@router.get("/talent/port/{id}")
def port_detail(id:int,db: Session = Depends(get_db)):
    course_by_id = crud.get_port(db=db, id=id)
    if course_by_id is None:
        raise HTTPException(status_code=404,detail="Portfolio by this id is not in database")
    return { "course":course_by_id}

@router.get("/talent/ports/{talent_id}")
def port_detail_status_wise(talent_id:int,db: Session = Depends(get_db)):
    course_week = crud.get_talents(db, talent_id)
    if not course_week:
        raise HTTPException(status_code=404,detail="Portfolio by this id is not in database")
    return { "Talent":course_week}

@router.delete("/talent/port/{id}")
async def delete_port(id: int, db: Session = Depends(get_db)):
    subject =  crud.get_port(db,id)
    if not subject:
        raise HTTPException(status_code=404,detail="Portfolio by this id is not in database")
    query = "Delete From ports WHERE id='"+str(id)+"'"
    db.execute(query)
    db.commit()
    return "deleted Succesfully"
