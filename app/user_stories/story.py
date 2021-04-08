
from typing import List
from fastapi import Depends,File, UploadFile, APIRouter
from fastapi_pagination.paginator import paginate
from sqlalchemy.orm import Session
from . import crud, models
#from courses_live.database import SessionCourse, some_engine
from app.talent.database import SessionLocal, engine
import shutil
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
S3_Key = "user-story" # change everywhere
S3_Bucket = 'cinedarbaar'
AWS_REGION = 'ap-south-1'
DESTINATION = "static/"
PUBLIC_DESTINATION = "https://cinedarbaar.s3.ap-south-1.amazonaws.com/"
s3_client = S3_SERVICE(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION)

@router.post("/story/")
async def create_story(story:str,fileobject: UploadFile= File(...), filename: str = Body(default=None), db: Session = Depends(get_db)):

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
        return crud.create_story(db=db,story=story,url=url)
    #return {"url": url,"status":status}

@router.get("/stories/" ,dependencies=[Depends(pagination_params)])
def story_list(db: Session = Depends(get_db)):
    story_all = crud.story_list(db=db)
    return paginate(story_all)

@router.get("/stories/{story_id}")
def story_detail(story_id:int,db: Session = Depends(get_db)):
    return crud.get_story(db=db, id=story_id)

@router.delete("/stories/{story_id}")
async def delete(story_id: int, db: Session = Depends(get_db)):
    deleted = await crud.delete(db, story_id)
    return {"deleted": deleted}