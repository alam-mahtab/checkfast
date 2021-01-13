from typing import List
from fastapi import Depends,File, UploadFile, APIRouter
from sqlalchemy.orm import Session
from cinematographer import crud, models
from writer.database import SessionLocal, engine
from cinematographer.schemas import CinematographerBase, CinematographerList
from cinematographer.models import Cinematographer
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

router.mount("/static", StaticFiles(directory="static"), name="static")
dirname = dirname(dirname(abspath(__file__)))
images_path = join(dirname, '/static')

@router.post("/cinematographer/")
def create_cinematographer(
    desc:str,name:str,file_pro: UploadFile= File(...), file_cover: UploadFile= File(...), db: Session = Depends(get_db)
):

    extension_pro = file_pro.filename.split(".")[-1] in ("jpg", "jpeg", "png") 
    if not extension_pro:
        return "Image must be jpg or png format!"
    suffix_pro = Path(file_pro.filename).suffix
    filename_pro = time.strftime( str(uuid.uuid4().hex) + "%Y%m%d-%H%M%S" + suffix_pro )
    with open("static/"+filename_pro, "wb") as image:
        shutil.copyfileobj(file_pro.file, image)
    url_profile = os.path.join(images_path, filename_pro)

    extension_cover = file_cover.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not extension_cover:
        return "Image must be jpg or png format!"
    suffix_cover =Path(file_cover.filename).suffix
    filename_cover = time.strftime( str(uuid.uuid4().hex) + "%Y%m%d-%H%M%S" + suffix_cover )
    with open("static/"+filename_cover, "wb") as image:
        shutil.copyfileobj(file_cover.file, image)
    url_cover = os.path.join(images_path, filename_cover)

    return crud.create_cinematographer(db=db,name=name,desc=desc,url_profile=url_profile,url_cover=url_cover)


@router.get("/cinematographers/" ,dependencies=[Depends(pagination_params)])
def cinematographer_list(db: Session = Depends(get_db)):
    cinematographer_all =crud.cinematographer_list(db=db)
    return paginate(cinematographer_all)

@router.get("/cinematographers/{cinematographer_id}")
def cinematographer_detail(cinematographer_id:int,db: Session = Depends(get_db)):
    return crud.get_cinematographer(db=db, id=cinematographer_id)

@router.delete("/cinematographers/{cinematographer_id}")
async def delete(cinematographer_id: int, db: Session = Depends(get_db)):
    deleted = await crud.delete(db, cinematographer_id)
    return {"deleted": deleted}