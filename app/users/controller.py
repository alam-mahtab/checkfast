from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.sql.functions import user
from sqlalchemy.orm import Session
from app.authentication import schemas, models
from app.utils import util
from app.All_Course import crud
from app.talent.database import database, SessionLocal, engine
# Pagination
from fastapi_pagination import Page, pagination_params
from fastapi_pagination.paginator import paginate
from app.authentication.models import Users
import pandas as pd
import re 
import cloudinary
import cloudinary.uploader
import os
import uuid
from pathlib import Path
import time
router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

models.Base.metadata.create_all(bind=engine)

from fastapi.param_functions import File, Body
from s3_events.s3_utils import S3_SERVICE
from dotenv import load_dotenv

env = os.getenv('ENV', 'dev')
env_file_name_dict = {
    "dev": ".dev.env",
}

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
S3_Bucket = os.getenv("S3_Bucket")
S3_Key = "project" # change everywhere
PUBLIC_DESTINATION = "https://cinedarbaar.s3.ap-south-1.amazonaws.com/"
s3_client = S3_SERVICE(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION)

@router.get("/users/me", response_model = schemas.UserList)
async def read_user_me(currentuser: schemas.UserList = Depends(util.get_current_active_user)):
    return currentuser

@router.get("/users/username", response_model= schemas.UserList)
async def find_user_by_username(username : str):
    query = Users.__table__.select().where(Users.username == username)
    return await database.fetch_one(query)

# @router.get("/user/{username}", response_model= schemas.UserList)
# async def find_email_by_username(username : str):
#     query = Users.__table__.select().where(Users.username == username)
#     return await database.fetch_one(query)

@router.get("/users/email",response_model = schemas.UserList)
async def find_user_by_email(email : str,currentuser: schemas.UserList = Depends(util.get_current_active_user)):
    query = Users.__table__.select().where(Users.email== email)
    return await database.fetch_one(query)

@router.delete("/users/username")
async def delete_user_by_username(username: str):
    query = Users.__table__.delete().where(Users.username == username)
    await database.execute(query)
    return {
        "status" : True,
        "message" : "This User Is been Delete"
    }

@router.get("/users/{userId}", response_model=schemas.UserList)
async def find_user_by_id(userId: str):
    query = Users.__table__.select().where(Users.id == userId)
    return await database.fetch_one(query)
    
@router.delete("/users/{userId}")
async def delete_user(user : schemas.UserDelete):
    query = Users.__table__.delete().where(Users.id == user.id)
    await database.execute(query=query)

    return {
        "status" : True,
        "message" : "This User Is been Delete"
    }


@router.get("/users",response_model=Page[schemas.UserList],dependencies=[Depends(pagination_params)])
async def find_all_user(
    currentuser : schemas.UserList = Depends(util.get_current_active_user),
):
    query = "select * from Users"
    user_all = await database.fetch_all(query=query, values={}) 
    return paginate(user_all)

# Wishlist

@router.post("/users/{userId}/wishlist")
def create_wishlist(client_id:str,course_id:int,db:Session=Depends(get_db)):
    return crud.create_wishlist(db=db,client_id=client_id,course_id=course_id)

@router.get("/users/{userId}/wishlist"  ,dependencies=[Depends(pagination_params)])
def wishlist_list(db: Session = Depends(get_db)):
    wishlist_all = crud.wishlist_list(db=db)
    return paginate(wishlist_all)
from copy import deepcopy
@router.get("/users/{userId}/wishlist/{id}")
async def comment_detail(id:str,db: Session = Depends(get_db)):
    course_by_id = crud.get_wishlist(db=db, id=id)
    if course_by_id is None:
        raise HTTPException(status_code=404,detail="Comment with this id is not in database")
    course = crud.get_wishlist_course_id(db=db, id=id)
    courses = []
    for i in course:
        print(i)
        course_by_id = crud.get_wishlist_course_by_id(db, i)
        courses.append(deepcopy(course_by_id))
    return courses

@router.delete("/users/{userId}/wishlist/{id}")
async def delete(id: int, db: Session = Depends(get_db)):
    deleted = await crud.delete_wishlist(db,id)
    return {"deleted": deleted}

# Project_undertaken
@router.post("/users/{userId}/project")
async def create_project(client_id:str,first_name:str,details:str,fileobject: UploadFile= File(...), filename: str = Body(default=None),db:Session=Depends(get_db)):
    if filename is None:
        #filename = generate_png_string()
        extension_pro = fileobject.filename.split(".")[-1] in ("jpg", "jpeg", "png") 
        if not extension_pro:
            return "Image must be jpg or png format!"
        suffix_pro = Path(fileobject.filename).suffix
        filename = time.strftime( str(uuid.uuid4().hex) + "%Y%m%d-%H%M%S" + suffix_pro )
    data = fileobject.file._file  # Converting tempfile.SpooledTemporaryFile to io.BytesIO
    uploads3 = await s3_client.upload_fileobj(bucket=S3_Bucket, key=S3_Key+"/"+filename, fileobject=data )
    if uploads3:
        url = os.path.join(PUBLIC_DESTINATION, S3_Key+"/"+filename)
        return crud.create_project(db=db,client_id=client_id,first_name=first_name,details=details,url=url)

@router.get("/users/{userId}/project"  ,dependencies=[Depends(pagination_params)])
def project_list(db: Session = Depends(get_db)):
    project_all = crud.project_list(db=db)
    print(project_all)
    return paginate(project_all)


@router.get("/users/{userId}/project/{id}")
def project_detail(id:str,db: Session = Depends(get_db)):
    course_by_id = crud.get_project(db=db, id=id)
    if course_by_id is None:
        raise HTTPException(status_code=404,detail="Project with this id is not in database")
    return course_by_id 

@router.delete("/users/{userId}/project/{id}")
async def delete_project(id: int, db: Session = Depends(get_db)):
    deleted = await crud.delete_project(db,id)
    return {"deleted": deleted}

# notes
@router.post("/users/{userId}/notes")
def create_notes(client_id:str,title:str,detail:str,db:Session=Depends(get_db)):
    return crud.create_notes(db=db,client_id=client_id,title=title,detail=detail)

@router.get("/users/{userId}/notes"  ,dependencies=[Depends(pagination_params)])
def notes_list(db: Session = Depends(get_db)):
    notes_all = crud.notes_list(db=db)
    print(notes_all)
    return paginate(notes_all)

@router.put("/users/{userId}/notes/{id}")
async def update_notes(
    client_id:str, id_s :int , title:str,detail:str,db:Session=Depends(get_db)
):  
    subject = crud.get_notes(db=db,title=title ,client_id=client_id)

    if not subject:
        raise HTTPException(status_code=404, detail="Course not found")
    # query = "UPDATE NOTES SET DETAIL = '"+str(detail)+"' WHERE CLIENT_ID = '"+str(client_id)+"' AND ID = '"+str(id)+"'" 

    # db.execute(query)
    # db.commit()
    query = models.Notes.__table__.update().\
        where(models.Notes.client_id == client_id and models.Notes.id == id_s).\
            values(
                title = title,
                detail=detail
            )
    await database.execute(query)
    return {"Result" : "Course Updated Succesfully"}

@router.get("/users/{userId}/notes/{id}")
def notes_detail(id:str,db: Session = Depends(get_db)):
    course_by_id = crud.get_notes(db=db, client_id=id)
    if course_by_id is None:
        raise HTTPException(status_code=404,detail="Notes with this id is not in database")
    return course_by_id

@router.delete("/users/{userId}/notes/{id}")
async def delete_notes(id: int, db: Session = Depends(get_db)):
    deleted = await crud.delete_notes(db,id)
    return {"deleted": deleted}