from typing import List
from fastapi import Depends,File, UploadFile, APIRouter
from sqlalchemy.orm import Session
from courses_live import crud, models
#from courses_live.database import SessionCourse, some_engine
from writer.database import SessionLocal, engine
from courses_live.schemas import LiveBase, LiveList
from courses_live.models import Live

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
    with open("static/"+filename, "wb") as image:
        shutil.copyfileobj(file.file, image)

    #url = str("media/"+file.filename)
    url = os.path.join(images_path, filename)
    return crud.create_live(db=db,name=name,title=title,desc=desc,url=url)


@router.get("/lives/" ,dependencies=[Depends(pagination_params)])
def live_list(db: Session = Depends(get_db)):
    live_all =crud.live_list(db=db)
    return paginate(live_all)

@router.get("/lives/{live_id}")
def live_detail(live_id:int,db: Session = Depends(get_db)):
    return crud.get_live(db=db, id=live_id)

@router.delete("/lives/{live_id}")
async def delete(live_id: int, db: Session = Depends(get_db)):
    deleted = await crud.delete(db, live_id)
    return {"deleted": deleted}