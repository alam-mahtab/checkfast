from typing import Dict, List
from fastapi import Depends,File, UploadFile, APIRouter, HTTPException, status
from fastapi.param_functions import File, Body
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
import boto3
from fastapi.responses import JSONResponse
from s3_events.s3_utils import S3_SERVICE
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

models.Base.metadata.create_all(bind=engine)
from .files import generate_png_string
# from .files import s3, AWS_S3_BUCKET_NAME, upload_file_to_bucket

# PUBLIC_DESTINATION = "https://cinedarbaar.s3.ap-south-1.amazonaws.com/courses"
# from random import randint
# gid = randint(100000,1000000)
# rec = ("course_video"+str(gid))
# @router.post('/api/customer/generate/upload', name='Upload CSV to AWS S3 Bucket',status_code=201)
# async def post_upload_user_csv(file_obj: UploadFile = File(...), filename:str=None):
#         upload_obj = upload_file_to_bucket(s3_client=s3(),
#                                            file_obj=file_obj.file,
#                                            bucket=AWS_S3_BUCKET_NAME,
#                                            folder='courses',  # To Be updated
#                                            object_name=file_obj.filename)
#         if upload_obj:
#             url = os.path.join(PUBLIC_DESTINATION, file_obj.filename)
#             print(url)
#             return JSONResponse(content="Object has been uploaded to bucket successfully",
#                                 status_code=status.HTTP_201_CREATED)
#         else:
#             raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                                 detail="File could not be uploaded")
from dotenv import load_dotenv

env = os.getenv('ENV', 'dev')
env_file_name_dict = {
    "dev": ".dev.env",
}

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
S3_Bucket = os.getenv("S3_Bucket")
S3_Key = "courses" # change everywhere
PUBLIC_DESTINATION = "https://cinedarbaar.s3.ap-south-1.amazonaws.com/"
s3_client = S3_SERVICE(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION)
#s3_client = boto3.resource('s3',aws_access_key_id=access_key,aws_secret_access_key=secret_access_key)
#S3_Bucket = s3_client.Bucket('cinedarbaar')



# @router.post("/upload", status_code=200, description="***** Upload png asset to S3 *****")
# async def upload(fileobject: UploadFile = File(...), filename: str = Body(default=None)):
#     if filename is None:
#         #filename = generate_png_string()
#         extension_pro = fileobject.filename.split(".")[-1] in ("jpg", "jpeg", "png") 
#         if not extension_pro:
#             return "Image must be jpg or png format!"
#         suffix_pro = Path(fileobject.filename).suffix
#         filename = time.strftime( str(uuid.uuid4().hex) + "%Y%m%d-%H%M%S" + suffix_pro )
#     data = fileobject.file._file  # Converting tempfile.SpooledTemporaryFile to io.BytesIO
#     uploads3 = await s3_client.upload_fileobj(bucket=S3_Bucket, key=S3_Key + filename, fileobject=data)
#     if uploads3:
#         s3_url = f"https://{S3_Bucket}.s3.{AWS_REGION}.amazonaws.com/{S3_Key}{filename}"
#         print(s3_url)
#         #doc = [{"image_url": s3_url}]
#         return s3_url
#     else:
#         raise HTTPException(status_code=400, detail="Failed to upload in S3")



# @router.post("/course/")
# def create_course(
#     title:str,description:str,name:str,price:int,type:str,short_desc:str,module:str,status:int,file: UploadFile= File(...),  db: Session = Depends(get_db)
# ):
#     #content_type = mimetypes.guess_type(fpath)[0]
#     extension_pro = file.filename.split(".")[-1] in ("jpg", "jpeg", "png") 
#     if not extension_pro:
#         return "Image must be jpg or png format!"
#     suffix_pro = Path(file.filename).suffix
#     filename = time.strftime( str(uuid.uuid4().hex) + "%Y%m%d-%H%M%S" + suffix_pro )
#     fullpath = os.path.join(DESTINATION, filename)
    
#     # result = cloudinary.uploader.upload(file.file)
#     # url = result.get("url")
#     with open(fullpath, "wb") as image:
#         shutil.copyfileobj(file.file, image)
    
#     with open(fullpath, 'rb') as data:
#         bucket.upload_fileobj(data, key+"/"+filename, ExtraArgs={'ACL': 'public-read'})
#     url = os.path.join(PUBLIC_DESTINATION, key+"/"+filename)
#     print(url)
#     return crud.create_course(db=db,name=name,title=title,description=description,price=price,short_desc=short_desc,module=module,url=url,type=type,status=status)

@router.post("/course/")
async def create_course(
    title:str,description:str,name:str,price:int,type:str,short_desc:str,module:str,status:int,fileobject: UploadFile= File(...), filename: str = Body(default=None), db: Session = Depends(get_db)
):
    if filename is None:
        #filename = generate_png_string()
        extension_pro = fileobject.filename.split(".")[-1] in ("jpg", "jpeg", "png") 
        if not extension_pro:
            return "Image must be jpg or png format!"
        suffix_pro = Path(fileobject.filename).suffix
        filename = time.strftime( str(uuid.uuid4().hex) + "%Y%m%d-%H%M%S" + suffix_pro )
    data = fileobject.file._file  # Converting tempfile.SpooledTemporaryFile to io.BytesIO
    uploads3 = await s3_client.upload_fileobj(bucket=S3_Bucket, key=S3_Key+"/"+filename, fileobject=data)
    if uploads3:
        url = os.path.join(PUBLIC_DESTINATION, S3_Key+"/"+filename)
        #url = f"https://{S3_Bucket}.s3.{AWS_REGION}.amazonaws.com/{S3_Key}{filename}"
        print(url)
        #doc = [{"image_url": s3_url}]
        return crud.create_course(db=db,name=name,title=title,description=description,price=price,short_desc=short_desc,module=module,url=url,type=type,status=status)
    else:
        raise HTTPException(status_code=400, detail="Failed to upload in S3")

@router.put("/course/{id}")
async def update_course(
    id:int,title:str,description:str,name:str,price:int,type:str,short_desc:str,module:str,status:int,fileobject: UploadFile= File(...), filename: str = Body(default=None), db: Session = Depends(get_db)
):
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
        subject =  crud.get_course(db,id)
        if not subject:
            raise HTTPException(status_code=404, detail="Course not found")
        query = "UPDATE courses SET title='"+str(title)+"' , name='"+str(name)+"' , description='"+str(description)+"' , price='"+str(price)+"' , short_desc='"+str(short_desc)+"', module ='"+str(module)+"', type ='"+str(type)+"', status='"+str(status)+"', url='"+str(url)+"' WHERE id='"+str(id)+"'"
        db.execute(query)
        db.commit()
        return {"Result" : "Course Updated Succesfully"}
    else:
        raise HTTPException(status_code=400, detail="Failed to upload in S3")

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