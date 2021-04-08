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
AWS_ACCESS_KEY_ID = "AKIA2O3WJVIG42BHMUPF"
AWS_SECRET_ACCESS_KEY = "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"
S3_Key = "resource" # change everywhere
S3_Bucket = 'cinedarbaar'
AWS_REGION = 'ap-south-1'
DESTINATION = "static/"
PUBLIC_DESTINATION = "https://cinedarbaar.s3.ap-south-1.amazonaws.com/"
s3_client = S3_SERVICE(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION)
 
# @router.post("/course/resource")
# async def create_learn(
#     course_id:int,fileobject: UploadFile= File(...), filename: str = Body(default=None), db: Session = Depends(get_db)
# ):  
#     if filename is None:
#         #filename = generate_png_string()
#         extension_pro = fileobject.filename.split(".")[-1] in ("pdf", "docx") 
#         if not extension_pro:
#             return "Image must be jpg or png format!"
#         suffix_pro = Path(fileobject.filename).suffix
#         filename = time.strftime( str(uuid.uuid4().hex) + "%Y%m%d-%H%M%S" + suffix_pro )
#     data = fileobject.file._file  # Converting tempfile.SpooledTemporaryFile to io.BytesIO
#     uploads3 = await s3_client.upload_fileobj(bucket=S3_Bucket, key=S3_Key+"/"+filename, fileobject=data )
#     if uploads3:
#         pdf_url = os.path.join(PUBLIC_DESTINATION, S3_Key+"/"+filename)
#         return crud.create_resource(db=db,pdf_url=pdf_url,course_id=course_id)

# @router.put("/course/resource/{id}")
# async def update_learn(
#     id:int,course_id:int,fileobject: UploadFile= File(...), filename: str = Body(default=None), db: Session = Depends(get_db)
# ):  
#     if filename is None:
#         #filename = generate_png_string()
#         extension_pro = fileobject.filename.split(".")[-1] in ("jpg", "jpeg", "png") 
#         if not extension_pro:
#             return "Image must be jpg or png format!"
#         suffix_pro = Path(fileobject.filename).suffix
#         filename = time.strftime( str(uuid.uuid4().hex) + "%Y%m%d-%H%M%S" + suffix_pro )
#     data = fileobject.file._file  # Converting tempfile.SpooledTemporaryFile to io.BytesIO
#     uploads3 = await s3_client.upload_fileobj(bucket=S3_Bucket, key=S3_Key+"/"+filename, fileobject=data )
#     if uploads3:
#         pdf_url = os.path.join(PUBLIC_DESTINATION, S3_Key+"/"+filename)
#         subject =  crud.get_resorce(db,id)
#         if not subject:
#             raise HTTPException(status_code=404, detail="Course not found")
#         query = "UPDATE resources SET course_id='"+str(course_id)+"' , pdf_url='"+str(pdf_url)+"' WHERE id='"+str(id)+"'"
#         db.execute(query)
#         db.commit()
#     return {"Result" : "Module Updated Succesfully"}

@router.post("/course/resource")
async def create_learn(
    course_id:int,pdf_url:str, db: Session = Depends(get_db)
):
    return crud.create_resource(db=db,course_id=course_id,pdf_url=pdf_url)

@router.put("/course/resource/{id}")
async def update_learn(
    id:int,course_id:int, pdf_url:str, db: Session = Depends(get_db)
):
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
