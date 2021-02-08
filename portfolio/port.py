
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

@router.post("/port/")
def create_port(status:int,file: UploadFile= File(...), db: Session = Depends(get_db)):

    # extension = file.filename.split(".")[-1] in ("mp4", "3gp")
    # if not extension:
    #     return "video must be mp4 or 3gp format!"
    
    # outputImage = Image.fromarray(sr_img)  
    suffix = Path(file.filename).suffix
    filename = time.strftime( str(uuid.uuid4().hex) + "%Y%m%d-%H%M%S" + suffix )
    with open("static/"+filename, "wb") as video:
        shutil.copyfileobj(file.file, video)

    #url = str("media/"+file.filename)
    url = os.path.join(images_path, filename)
    crud.create_port(db=db,status=status,url=url)
    return {"url": url,"status":status}

@router.get("/ports/" ,dependencies=[Depends(pagination_params)])
def port_list(db: Session = Depends(get_db)):
    port_all = crud.port_list(db=db)
    return paginate(port_all)

@router.get("/ports/{port_id}")
def port_detail(port_id:int,db: Session = Depends(get_db)):
    return crud.get_port(db=db, id=port_id)

@router.delete("/ports/{port_id}")
async def delete(port_id: int, db: Session = Depends(get_db)):
    deleted = await crud.delete(db, port_id)
    return {"deleted": deleted}