from typing import Dict, List
from fastapi import Depends,File, UploadFile, APIRouter, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from courses_live.database import SessionCourse, some_engine
import shutil
from coursebysubject.schemas import SubjectBase, SubjectUpdate
from coursebysubject.models import Subject
import datetime
#from coursebysubject.models import subjects
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

@router.put("/subjects/{subject_id}", response_model=schemas.SubjectBase, status_code=200)
async def put_note(subject_id: int, subject: schemas.SubjectUpdate,file: UploadFile= File(...), db: Session = Depends(get_db)):
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
    db_subject = schemas.SubjectUpdate(db=db,id =id, title=subject.title, desc=subject.desc,name=subject.name, url=url)

    return crud.update_subject(db=db, note=db_subject) # Added return

@router.patch("/subjects/{subject_id}", response_model=schemas.SubjectUpdate, status_code=200)
async def patch_note(subject_id: int, subject: schemas.SubjectBase, db: Session = Depends(get_db)):

    print(subject_id)
    print(subject.title)
    print(subject.description)
    db_subject = schemas.SubjectUpdate(id =subject_id, title= subject.title, desc=subject.desc, name= subject.name, url=subject.url)

    return crud.update_subject(db=db, note=db_subject) # Added return
    
# @router.put("/subjects/{subject_id}")
# async def update_subject(
#     #user : schemas.SubjectUpdate,
#     subject_id: int,
#     title:str,desc:str,name:str,file: UploadFile= File(...), db: Session = Depends(get_db)
# ):
#     extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
#     if not extension:
#         return "Image must be jpg or png format!"
    
#     # outputImage = Image.fromarray(sr_img)  
#     suffix = Path(file.filename).suffix
#     filename = time.strftime( str(uuid.uuid4().hex) + "%Y%m%d-%H%M%S" + suffix )
#     with open("static/"+filename, "wb") as image:
#         shutil.copyfileobj(file.file, image)

#     #url = str("media/"+file.filename)
#     url = os.path.join(images_path, filename)
#     subject =  crud.get_subject(db,id)
#     if not subject:
#         raise HTTPException(status_code=404, detail="comment not found")

#     return await crud.update_subject(db=db,name=name,title=title,desc=desc,url=url)
#     #return {"updated" : updated}


# @router.put("/subjects/{id}/", response_model=SubjectBase)
# async def update_subject(payload: SubjectUpdate,db: Session = Depends(get_db)):
#     subject = await crud.get_subject(db,id)
#     if not subject:
#         raise HTTPException(status_code=404, detail="comment not found")

#     subject_id = await crud.put(id, payload)

#     response_object ={
#         "id": subject_id,
#         "Name": payload.name,
#         "title": payload.title,
#         "description": payload.desc,
#    }
#     return response_object(**Dict)

# @router.put("/subjects/{id}",response_model=SubjectList)
# async def update_subject(subject : SubjectUpdate, db: Session = Depends(get_db)):
    
#     update = await crud.put_sub(db, subject, models.Subject.id)

#     return {"update" : update}
#     #return await find_user_by_id(user.id)