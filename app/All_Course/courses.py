from typing import Dict, List
from fastapi import Depends,File, UploadFile, APIRouter, HTTPException
from sqlalchemy.orm import Session
from . import crud, schemas
from app.authentication import models
#from courses_live.database import SessionCourse, some_engine
from app.talent.database import SessionLocal, engine,database
import shutil
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
import cloudinary
import cloudinary.uploader

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

current_file = Path(__file__)
current_file_dir = current_file.parent
project_root = current_file_dir.parent
project_root_absolute = project_root.resolve()
static_root_absolute = project_root_absolute / "static" 
 
@router.post("/course/")
def create_course(
    title:str,desc:str,name:str,price:int,type:str,short_desc:str,module:str,status:int,file: UploadFile= File(...), db: Session = Depends(get_db)
):

    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not extension:
        return "Image must be jpg or png format!"
    
    # outputImage = Image.fromarray(sr_img)  
    suffix = Path(file.filename).suffix
    filename = time.strftime( str(uuid.uuid4().hex) + "%Y%m%d-%H%M%S" + suffix )
    result = cloudinary.uploader.upload(file.file)
    url = result.get("url")
    return crud.create_course(db=db,name=name,title=title,desc=desc,price=price,short_desc=short_desc,module=module,url=url,type=type,status=status)

@router.put("/course/{id}")
async def update_course(
    id:int,title:str,desc:str,name:str,price:int,type:str,short_desc:str,module:str,status:int,file: UploadFile= File(...), db: Session = Depends(get_db)
):
    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not extension:
        return "Image must be jpg or png format!"
    
    # outputImage = Image.fromarray(sr_img)  
    suffix = Path(file.filename).suffix
    filename = time.strftime( str(uuid.uuid4().hex) + "%Y%m%d-%H%M%S" + suffix )
    result = cloudinary.uploader.upload(file.file)
    url = result.get("url")
    subject =  crud.get_course(db,id)
    if not subject:
        raise HTTPException(status_code=404, detail="Course not found")
    #'select * from USERS where email='+"'"+str(username)+"'"+' and PASSWORD='+"'"+str(password)+"'"
    query = "UPDATE courses SET title='"+str(title)+"' , name='"+str(name)+"' , desc='"+str(desc)+"' , price='"+str(price)+"' , short_desc='"+str(short_desc)+"', module ='"+str(module)+"', type ='"+str(type)+"', status='"+str(status)+"', url='"+str(url)+"' WHERE id='"+str(id)+"'"
    db.execute(query)
    db.commit()
    return {"Result" : "Course Updated Succesfully"}
#     return await crud.update_course(db=db,name=name,title=title,desc=desc,price=price,url=url,type=type,status=status)
#     #return {"update": update}

@router.get("/courses/"  ,dependencies=[Depends(pagination_params)])
def course_list(db: Session = Depends(get_db)):
    course_all = crud.course_list(db=db)
    return paginate(course_all)

@router.get("/courses/{courses_id}")
def course_detail(courses_id:int,db: Session = Depends(get_db)):
    course_by_id = crud.get_course(db=db, id=courses_id)
    comments = db.query(models.Comment).filter(models.Comment.courses_id == courses_id)
    active_comment = comments.filter(models.Comment.is_active == True).all()
    if course_by_id is None:
        raise HTTPException(status_code=404,detail="Course by this id is not in database")
    return { "course":course_by_id, "active_comment":active_comment }

@router.delete("/courses/{courses_id}")
async def delete(courses_id: int, db: Session = Depends(get_db)):
    subject =  crud.get_course(db=db, id=courses_id)
    if not subject:
        raise HTTPException(status_code=404,detail="Course by this id is not in database")
    query = "Delete From weeks WHERE id='"+str(courses_id)+"'"
    db.execute(query)
    db.commit()
    return "deleted Succesfully"
# @router.delete("/courses/{courses_id}")
# async def delete(subject_id: int, db: Session = Depends(get_db)):
#     deleted = await crud.delete(db, subject_id)
#     return {"deleted": deleted}

# 1.Master Course
@router.get("/Master/"  ,dependencies=[Depends(pagination_params)])
def master_list(db: Session = Depends(get_db)):
    master_all = crud.master_list(db=db)
    return paginate(master_all)

# 2.Extensive Course
@router.get("/Extensive/"  ,dependencies=[Depends(pagination_params)])
def extensive_list(db: Session = Depends(get_db)):
    extensive_all = crud.extensive_list(db=db)
    return paginate(extensive_all)

# 3.Micro Course
@router.get("/Micro/"  ,dependencies=[Depends(pagination_params)])
def micro_list(db: Session = Depends(get_db)):
    micro_all = crud.micro_list(db=db)
    return paginate(micro_all)

# 4.Live Course
@router.get("/Live/"  ,dependencies=[Depends(pagination_params)])
def live_list(db: Session = Depends(get_db)):
    live_all = crud.live_list(db=db)
    return paginate(live_all)

# 5.Profession Course
@router.get("/Profession/"  ,dependencies=[Depends(pagination_params)])
def profession_list(db: Session = Depends(get_db)):
    profession_all = crud.profession_list(db=db)
    return paginate(profession_all)

# 6.Subject Course
@router.get("/Subject/"  ,dependencies=[Depends(pagination_params)])
def subject_list(db: Session = Depends(get_db)):
    subject_all = crud.subject_list(db=db)
    return paginate(subject_all)

# 7.Free Course
@router.get("/Free/"  ,dependencies=[Depends(pagination_params)])
def free_list(db: Session = Depends(get_db)):
    free_all = crud.master_list(db=db)
    return paginate(free_all)

# Comment Section

@router.post("/courses/{courses_id}/comment")
def create_comment(name:str,Message:str,courses_id:int,db:Session=Depends(get_db)):
    return crud.create_comment(db=db,name=name,Message=Message,courses_id=courses_id)

@router.get("/courses/{courses_id}/comment"  ,dependencies=[Depends(pagination_params)])
def comment_list(db: Session = Depends(get_db)):
    comment_all = crud.comment_list(db=db)
    return paginate(comment_all)

@router.get("/courses/{courses_id}/comment/{id}")
def comment_detail(id:int,db: Session = Depends(get_db)):
    course_by_id = crud.get_comment(db=db, id=id)
    # comments = db.query(models.Comment).filter(models.Comment.courses_id == courses_id)
    #active_comment = comments.filter(models.Comment.is_active == True).all()
    if course_by_id is None:
        raise HTTPException(status_code=404,detail="Comment with this id is not in database")
    return { "comments":course_by_id, }#"active_comment":active_comment }