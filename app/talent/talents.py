from typing import List
from fastapi import Depends,File, UploadFile, APIRouter, HTTPException
from sqlalchemy.orm import Session
from . import crud, models
from .database import SessionLocal, engine
from .schemas import TalentBase, TalentList
from .models import Talent
# Pagination
from fastapi_pagination import Page, pagination_params
from fastapi_pagination.paginator import paginate
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

models.Base.metadata.create_all(bind=engine)

import uuid
from pathlib import Path
import time
#from fastapi.staticfiles import StaticFiles
from starlette.staticfiles import StaticFiles
import os
from os.path import dirname, abspath, join
import shutil

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
S3_Key = "talents" # change everywhere
PUBLIC_DESTINATION = "https://cinedarbaar.s3.ap-south-1.amazonaws.com/"
s3_client = S3_SERVICE(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION)

@router.post("/talent/")
async def create_talent(
    description:str,name:str,type:str,status:int,profile:str,file_pro: UploadFile= File(...), file_cover: UploadFile= File(...),filename1: str = Body(default=None), filename2: str = Body(default=None), db: Session = Depends(get_db)
):

    if filename1 is None:
        #filename = generate_png_string()
        extension_pro = file_pro.filename.split(".")[-1] in ("jpg", "jpeg", "png") 
        if not extension_pro:
            return "Image must be jpg or png format!"
        suffix_pro = Path(file_pro.filename).suffix
        filename = time.strftime( str(uuid.uuid4().hex) + "%Y%m%d-%H%M%S" + suffix_pro )
    data = file_pro.file._file  # Converting tempfile.SpooledTemporaryFile to io.BytesIO
    uploads3 = await s3_client.upload_fileobj(bucket=S3_Bucket, key=S3_Key+"/"+filename, fileobject=data )
    if uploads3:
        url_profile = os.path.join(PUBLIC_DESTINATION, S3_Key+"/"+filename)
    else:
        raise HTTPException(status_code=400, detail="Failed to upload in S3")

    if filename2 is None:
        #filename = generate_png_string()
        extension_pro = file_cover.filename.split(".")[-1] in ("jpg", "jpeg", "png") 
        if not extension_pro:
            return "Image must be jpg or png format!"
        suffix_pro = Path(file_cover.filename).suffix
        filename = time.strftime( str(uuid.uuid4().hex) + "%Y%m%d-%H%M%S" + suffix_pro )
    data = file_cover.file._file  # Converting tempfile.SpooledTemporaryFile to io.BytesIO
    uploads3 = await s3_client.upload_fileobj(bucket=S3_Bucket, key=S3_Key+"/"+filename, fileobject=data )
    if uploads3:
        url_cover = os.path.join(PUBLIC_DESTINATION, S3_Key+"/"+filename)

        return crud.create_talent(db=db,name=name,description=description,profile=profile,url_profile=url_profile,url_cover=url_cover,type=type,status=status)
    else:
        raise HTTPException(status_code=400, detail="Failed to upload in S3")

@router.put("/talent/{id}")
async def update_talent(
    id:int,description:str,name:str,type:str,status:int,profile:str,file_pro: UploadFile= File(...), file_cover: UploadFile= File(...),filename1: str = Body(default=None), filename2: str = Body(default=None), db: Session = Depends(get_db)
):

    if filename1 is None:
        #filename = generate_png_string()
        extension_pro = file_pro.filename.split(".")[-1] in ("jpg", "jpeg", "png") 
        if not extension_pro:
            return "Image must be jpg or png format!"
        suffix_pro = Path(file_pro.filename).suffix
        filename = time.strftime( str(uuid.uuid4().hex) + "%Y%m%d-%H%M%S" + suffix_pro )
    data = file_pro.file._file  # Converting tempfile.SpooledTemporaryFile to io.BytesIO
    uploads31 = await s3_client.upload_fileobj(bucket=S3_Bucket, key=S3_Key+"/"+filename, fileobject=data )
    if uploads31:
        url_profile = os.path.join(PUBLIC_DESTINATION, S3_Key+"/"+filename)
    else:
        raise HTTPException(status_code=400, detail="Failed to upload in S3")

    if filename2 is None:
        #filename = generate_png_string()
        extension_pro = file_cover.filename.split(".")[-1] in ("jpg", "jpeg", "png") 
        if not extension_pro:
            return "Image must be jpg or png format!"
        suffix_pro = Path(file_cover.filename).suffix
        filename = time.strftime( str(uuid.uuid4().hex) + "%Y%m%d-%H%M%S" + suffix_pro )
    data = file_cover.file._file  # Converting tempfile.SpooledTemporaryFile to io.BytesIO
    uploads32 = await s3_client.upload_fileobj(bucket=S3_Bucket, key=S3_Key+"/"+filename, fileobject=data )
    if uploads32:
        url_cover = os.path.join(PUBLIC_DESTINATION, S3_Key+"/"+filename)
        subject =  crud.get_talent(db,id)
        if not subject:
            raise HTTPException(status_code=404, detail="Talents not found")
        query = "UPDATE talents SET url_profile='"+str(url_profile)+"' , description='"+str(description)+"' , profile ='"+str(profile)+"', status='"+str(status)+"', url_cover='"+str(url_cover)+"' WHERE id='"+str(id)+"'"
        db.execute(query)
        db.commit()
        return {"Result" : "Talent Updated Succesfully"}
    else:
        raise HTTPException(status_code=400, detail="Failed to upload in S3")

@router.get("/talents/" ,dependencies=[Depends(pagination_params)])
def talent_list(db: Session = Depends(get_db)):
    talent_all =crud.talent_list(db=db)
    return paginate(talent_all)

@router.get("/talents/{talent_id}")
def talent_detail(talent_id:int,db: Session = Depends(get_db)):
    talent_by_id =  crud.get_talent(db=db, id=talent_id)
    if talent_by_id is None:
        raise HTTPException(status_code=404,detail="Course by this id is not in database")
    return {"talent":talent_by_id}

@router.delete("/talents/{talent_id}")
async def delete(talent_id: int, db: Session = Depends(get_db)):
    deleted = await crud.delete(db, talent_id)
    return {"deleted": deleted}

# 1.Writer
@router.get("/Witer/" ,dependencies=[Depends(pagination_params)])
def writer_list(db: Session = Depends(get_db)):
    writer_all =crud.writer_list(db=db)
    return paginate(writer_all)
# 2.Director
@router.get("/Director/" ,dependencies=[Depends(pagination_params)])
def director_list(db: Session = Depends(get_db)):
    director_all =crud.director_list(db=db)
    return paginate(director_all)
# 3.Actor
@router.get("/Actor/" ,dependencies=[Depends(pagination_params)])
def actor_list(db: Session = Depends(get_db)):
    actor_all =crud.actor_list(db=db)
    return paginate(actor_all)
# 4.Cinematographer
@router.get("/Cinematographer/" ,dependencies=[Depends(pagination_params)])
def cinematographer_list(db: Session = Depends(get_db)):
    cinematographer_all =crud.cinematographer_list(db=db)
    return paginate(cinematographer_all)
# 5.Editor
@router.get("/Editor/" ,dependencies=[Depends(pagination_params)])
def editor_list(db: Session = Depends(get_db)):
    editor_all =crud.editor_list(db=db)
    return paginate(editor_all)
# 6.SoundEditor
@router.get("/Soundeditor/" ,dependencies=[Depends(pagination_params)])
def sound_editor_list(db: Session = Depends(get_db)):
    sound_all =crud.soundeditor_list(db=db)
    return paginate(sound_all)
# 7.Filmmaker
@router.get("/Filmmaker/" ,dependencies=[Depends(pagination_params)])
def filmmaker_list(db: Session = Depends(get_db)):
    filmmaker_all =crud.filmmaker_list(db=db)
    return paginate(filmmaker_all)
# 8.Videographer
@router.get("/Videographer/" ,dependencies=[Depends(pagination_params)])
def videographer_list(db: Session = Depends(get_db)):
    videographer_all =crud.videographer_list(db=db)
    return paginate(videographer_all)
# 9.FilmEditor
@router.get("/Filmediting/" ,dependencies=[Depends(pagination_params)])
def filmediting_list(db: Session = Depends(get_db)):
    filmediting_all =crud.filmediting_list(db=db)
    return paginate(filmediting_all)