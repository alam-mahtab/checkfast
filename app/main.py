from app.configs.appinfo import setting

#from configs.connection import database
from app.talent.database import database
from fastapi import FastAPI, Request, Depends, UploadFile, File

from .configs import dbinfo,appinfo
import time
from fastapi.middleware.cors import CORSMiddleware
#import aiofiles
#from aiofiles import stat as aio_stat
import asyncio
#from fastapi.staticfiles import StaticFiles
from starlette.staticfiles import StaticFiles

tags_metadata = [
    {   "name": "Auth",
        "description": "Operations with authentication. The **login** logic is also here.", },
    {   "name": "Users",
        "description": "Manage users. So _fancy_ they have their own docs.", },
    {   "name": "Awards",
        "description": "Operations with awards section in talent & courses. sorting done by status",},
    {   "name": "Filmography",
        "description": "Operations with filmography section in talent & courses. sorting done by status",    },
    {   "name": "Portfolio",
        "description": "Operations with portfolio section in talent & courses. sorting done by status",    },
    {   "name": "Work",
        "description": "Operations with 1.work with us, 2.affiliate, 3.partnership. status = 1 means (work with us) and so on",    },
    
]

app = FastAPI(
    openapi_tags=tags_metadata,
    title="CineDarbaar Project",
    description="This is the Backend Of the Educational Website deals with Film industry",
    version="0.0.0",
)

# origins = [
#     "http://checkfast.herokuapp.com/docs",
#     "https://checkfast.herokuapp.com/docs",
#     "uvicorn main:app --host=0.0.0.0 --port=${PORT:-5000}",
#     "uvicorn main:app --host=0.0.0.0 --port=${PORT:-5000}/docs",
#     "http://0.0.0.0:5000",
#     "http://0.0.0.0:5000/docs",
#     "http://localhost",
#     "http://localhost:8080",
#     "http://localhost:8000",
#     "http://localhost:4200",
#     "http://localhost:5000",
#     "http://127.0.0.1:5000",
#     "http://127.0.0.1:4200",
#     "http://127.0.0.1:8080",
#     "http://127.0.0.1:8000",
# ]
#origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    #["DELETE", "GET", "POST", "PUT"],
    allow_headers=["*"],
)


def app_setting():
    return appinfo.setting()

@app.get("/app/info", tags =["App"])
async def app_info(setting: appinfo.setting = Depends(app_setting)):
    
    return {
        "app_name" : setting.app_name,
        "app_version" : setting.app_version,
        "app_framework" : setting.app_framework,
        "app_date" : setting.app_date,
    }


@app.middleware("http")
async def add_process_time_header(request : Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    response.headers['X-Process-Time'] = str(process_time)

    return response


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

from app.authentication import controller as authController
app.include_router(authController.router, tags =["Auth"])

from app.users import controller as userController
app.include_router(userController.router, tags =["Users"])

from app.module import router as weekmodule
app.include_router(weekmodule.router, tags=['Week wise module'])

from app.honour import router as honour
app.include_router(honour.router, tags=['Awards Filmography'])

from app.AboutCourse import router as AboutCourse
app.include_router(AboutCourse.router, tags=['AboutCourse'])

from app.Learn import router as Learn
app.include_router(Learn.router, tags=['Learn'])

from app.Lesson import router as Lesson
app.include_router(Lesson.router, tags=['Lesson'])
#new code
from app.api import ping
app.include_router(ping.router)

# payment
from app.Payment import donate
app.include_router(donate.router, tags=["Payments"])

# For Course 
from app.All_Course import courses
app.include_router(courses.router, prefix="/course", tags=["Courses"])

# Talent And Courses
from app.talent import talents
app.include_router(talents.router, prefix="/talents", tags=["Talents"])
# For work_with_us
from app.work_with_us import work
app.include_router(work.router, prefix="/work", tags=["Work"])

# For Inquiry
from app.inquiry_form import inquiry
app.include_router(inquiry.router, prefix="/inquiry", tags=["Inquiry"])

# For FAQS
from app.Faqs import question
app.include_router(question.router, prefix="/faq", tags=["FAQS"])

# # For Awards
# from app.awards import award
# app.include_router(award.router, prefix="/award", tags=["Awards"])

# # For Filmography
# from app.filmography import filmo
# app.include_router(filmo.router, prefix="/filmo", tags=["Filmography"])

# # For Portfolio
# from app.portfolio import port
# app.include_router(port.router, prefix="/port", tags=["Portfolio"])



# For User Story
from app.user_stories import story
app.include_router(story.router, prefix="/story", tags=["Story"])



#image upload
import uuid
from pathlib import Path

import os
from os.path import dirname, abspath, join
import shutil
import aiofiles

# # S3
# import boto3
# from botocore.exceptions import NoCredentialsError

# ACCESS_KEY = ''
# SECRET_KEY = ''

# @app.post('upload')
# def upload():
#     s3 = boto3.client('s3')
#     with open("FILE_NAME", "rb") as f:
#     s3.upload_fileobj(f, "BUCKET_NAME", "OBJECT_NAME")
#     s3.upload_file(
#     'FILE_NAME', 'BUCKET_NAME', 'OBJECT_NAME',
#     ExtraArgs={'Metadata': {'mykey': 'myvalue'}}

# @app.post('upload')
# def upload_to_aws(file: UploadFile = local_file, bucket, s3_file):
#     s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
#                       aws_secret_access_key=SECRET_KEY)

#     try:
#         s3.upload_file(local_file, bucket, s3_file)
#         print("Upload Successful")
#         return True
#     except FileNotFoundError:
#         print("The file was not found")
#         return False
#     except NoCredentialsError:
#         print("Credentials not available")
#         return False


# uploaded = upload_to_aws('local_file', 'bucket_name', 's3_file_name')

app.mount("/static", StaticFiles(directory="static"), name="static")
dirname = dirname(dirname(abspath(__file__)))
images_path = join(dirname, '/static')

current_file = Path(__file__)
current_file_dir = current_file.parent
project_root = current_file_dir.parent
project_root_absolute = project_root.resolve()
static_root_absolute = project_root_absolute / "static" 
 
# @app.post("/cv2")
# async def get_image(request: Request, file: UploadFile = File(...)):
 
#    # extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
#     #if not extension:
#      #   return "Image must be jpg or png format!"  
#     suffix = Path(file.filename).suffix
#     filename = time.strftime( str(uuid.uuid4().hex) + "%Y%m%d-%H%M%S" + suffix )
    
#     with open("static/"+filename, "wb") as image:
#         shutil.copyfileobj(file.file, image)

#     #url = str("media/"+file.filename)
#     file_path = os.path.join(images_path, filename)
#     print(file_path)
#     client_host = request.client.host
#     return {"url": file_path,"client_host": client_host}

# from fastapi.responses import StreamingResponse

# some_file_path = "C:\\Users\\Ehtesham Hassan\\Desktop\\Testfast\\8.mp4" #os.path.join(UPLOAD_FOLDER, "1.mp4")

# @app.get("/video")
# def video():
#     file_like = open(some_file_path, mode="rb")
    
#     return StreamingResponse(file_like, media_type="video/mp4")

# async def fake_video_streamer():
#     for i in range(10000):
#         yield b"some fake video bytes"


# @app.get("/stream")
# async def stream():
#     return StreamingResponse(fake_video_streamer())

# # Send mail
# from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
# from pydantic import EmailStr
# from pydantic import EmailStr, BaseModel
# from starlette.responses import JSONResponse
# from typing import List
# class EmailSchema(BaseModel):
#     email: List[EmailStr]


# conf = ConnectionConfig(
#     MAIL_USERNAME = "priyanka@mobirizer.com",
#     MAIL_PASSWORD = "123456789",
#     MAIL_FROM = "priyanka@mobirizer.com",
#     MAIL_PORT = 587,  
#     MAIL_SERVER = "smtpout.secureserver.net",
#     MAIL_TLS = True,
#     MAIL_SSL = False,
#     USE_CREDENTIALS = True
# )



# html = """
# <p>Hi this test mail using BackgroundTasks, thanks for using Fastapi-mail</p> 
# """


# @app.post("/email")
# async def simple_send(email: EmailSchema) -> JSONResponse:

#     message = MessageSchema(
#         subject="Fastapi-Mail module",
#         recipients=email.dict().get("email"),  # List of recipients, as many as you can pass 
#         body=html,
#         subtype="html"
#         )

#     fm = FastMail(conf)
#     await fm.send_message(message)
#     return JSONResponse(status_code=200, content={"message": "email has been sent"})    
    