
from typing import List
from fastapi import Depends,File, UploadFile, APIRouter
from fastapi_pagination.paginator import paginate
from sqlalchemy.orm import Session
from coursebytutor import crud, models
from coursebytutor.database import SessionLocal, engine
import shutil
from coursebytutor.schemas import TutorBase, TutorList
from coursebytutor.models import Tutor
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

router.mount("/static", StaticFiles(directory="static"), name="static")
dirname = dirname(dirname(abspath(__file__)))
images_path = join(dirname, '/static')

@router.post("/tutor/")
def create_tutor(
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
    return crud.create_tutor(db=db,name=name,title=title,desc=desc,url=url)

@router.get("/tutors/" ,dependencies=[Depends(pagination_params)])
def tutor_list(db: Session = Depends(get_db)):
    tutor_all = crud.tutor_list(db=db)
    return paginate(tutor_all)

@router.get("/tutors/{tutor_id}")
def tutor_detail(tutor_id:int,db: Session = Depends(get_db)):
    return crud.get_tutor(db=db, id=tutor_id)

@router.delete("/tutors/{tutor_id}")
async def delete(tutors_id: int, db: Session = Depends(get_db)):
    deleted = await crud.delete(db, tutors_id)
    return {"deleted": deleted}