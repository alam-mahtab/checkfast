
from typing import List
from fastapi import Depends,File, UploadFile, APIRouter
from sqlalchemy.orm import Session
from coursebysubject import crud, models
from coursebysubject.database import SessionLocal, engine
import shutil
from coursebysubject.schemas import SubjectBase, SubjectList
from coursebysubject.models import Subject
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

router.mount("/static", StaticFiles(directory="static"), name="static")
dirname = dirname(dirname(abspath(__file__)))
images_path = join(dirname, '/static')

@router.post("/subject/")
def create_subject(
    title:str,desc:str,name:str,file: UploadFile= File(...), db: Session = Depends(get_db)
):

    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not extension:
        return "Image must be jpg or png format!"
    
    # outputImage = Image.fromarray(sr_img)  
    suffix = Path(file.filename).suffix
    filename = time.strftime( str(uuid.uuid4().hex) + "%Y%m%d-%H%M%S" + suffix )
    with open("static/"+filename, "wb") as image:
        shutil.copyfileobj(file.file, image)

    #url = str("media/"+file.filename)
    url = os.path.join(images_path, filename)
    return crud.create_subject(db=db,name=name,title=title,desc=desc,url=url)

@router.get("/subjects/")
def subject_list(db: Session = Depends(get_db)):
    return crud.subject_list(db=db)

@router.get("/subjects/{subject_id}")
def subject_detail(subject_id:int,db: Session = Depends(get_db)):
    return crud.get_subject(db=db, id=subject_id)