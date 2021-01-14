from typing import List
from fastapi import Depends,File, UploadFile, APIRouter
from sqlalchemy.orm import Session
from coursebysubject import crud, models
from courses_live.database import SessionCourse, some_engine
import shutil
from coursebysubject.schemas import SubjectBase, SubjectList
from coursebysubject.models import Subject
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
    db = SessionCourse()
    try:
        yield db
    finally:
        db.close()

models.Base1.metadata.create_all(bind=some_engine)

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

@router.get("/subjects/"  ,dependencies=[Depends(pagination_params)])
def subject_list(db: Session = Depends(get_db)):
    subject_all = crud.subject_list(db=db)
    return paginate(subject_all)

@router.get("/subjects/{subject_id}")
def subject_detail(subject_id:int,db: Session = Depends(get_db)):
    return crud.get_subject(db=db, id=subject_id)

@router.delete("/subjects/{subject_id}")
async def delete(subject_id: int, db: Session = Depends(get_db)):
    deleted = await crud.delete(db, subject_id)
    return {"deleted": deleted}