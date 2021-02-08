
from typing import List
from fastapi import Depends,File, UploadFile, APIRouter
from fastapi_pagination.paginator import paginate
from sqlalchemy.orm import Session
from . import crud, models
#from courses_live.database import SessionCourse, some_engine
from talent.database import SessionLocal, engine
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

router.mount("/static", StaticFiles(directory="static"), name="static")
dirname = dirname(dirname(abspath(__file__)))
images_path = join(dirname, '/static')

@router.post("/story/")
def create_story(story:str,file: UploadFile= File(...), db: Session = Depends(get_db)):

    extension = file.filename.split(".")[-1] in ("jpg", "jpeg","png")
    if not extension:
        return "image must be mp4 or 3gp format!"
    suffix = Path(file.filename).suffix
    filename = time.strftime( str(uuid.uuid4().hex) + "%Y%m%d-%H%M%S" + suffix )
    with open("static/"+filename, "wb") as image:
        shutil.copyfileobj(file.file, image)

    #url = str("media/"+file.filename)
    url = os.path.join(images_path, filename)
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