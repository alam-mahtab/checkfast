from typing import List
from fastapi import Depends,File, UploadFile, APIRouter
from sqlalchemy.orm import Session
from courses_live import crud, models
from courses_live.database import SessionLocal, engine
from courses_live.schemas import LiveBase, LiveList
from courses_live.models import Live
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
#from fastapi.staticfiles import StaticFiles
import os
from os.path import dirname, abspath, join
import shutil

dirname = dirname(dirname(abspath(__file__)))
images_path = join(dirname, 'media')

@router.post("/live/")
def create_live(
    title:str,desc:str,name:str,file: UploadFile= File(...), db: Session = Depends(get_db)
):

    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not extension:
        return "Image must be jpg or png format!"
    
    # outputImage = Image.fromarray(sr_img)  
    suffix = Path(file.filename).suffix
    filename = time.strftime( str(uuid.uuid4().hex) + "%Y%m%d-%H%M%S" + suffix )
    with open("media/"+filename, "wb") as image:
        shutil.copyfileobj(file.file, image)

    #url = str("media/"+file.filename)
    url = os.path.join(images_path, filename)
    return crud.create_live(db=db,name=name,title=title,desc=desc,url=url)

@router.get("/lives/")
def live_list(db: Session = Depends(get_db)):
    return crud.live_list(db=db)

@router.get("/lives/{live_id}")
def live_detail(live_id:int,db: Session = Depends(get_db)):
    return crud.get_live(db=db, id=live_id)