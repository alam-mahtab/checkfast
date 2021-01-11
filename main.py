from configs.appinfo import setting

from configs.connection import database
from fastapi import FastAPI, Request, Depends, UploadFile, File

from configs import appinfo
import time
from fastapi.middleware.cors import CORSMiddleware
#import aiofiles
#from aiofiles import stat as aio_stat
import asyncio
#from fastapi.staticfiles import StaticFiles
from starlette.staticfiles import StaticFiles

app = FastAPI()

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
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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

from auth import controller as authController
app.include_router(authController.router, tags =["Auth"])

from users import controller as userController
app.include_router(userController.router, tags =["Users"])

#new code
from api import ping
app.include_router(ping.router)


# For Comments
from comment import comnotes
app.include_router(comnotes.router, prefix="/comnotes", tags=["Comment"])

# For Feeds
from feed import fnotes
app.include_router(fnotes.router, prefix="/fnotes", tags=["Feed"])

#For live course
from courses_live import live_course
app.include_router(live_course.router, prefix="/live_course", tags=["Live Course"])

# Course By tutor
# from coursebytutor import course_by_tutor
# app.include_router(course_by_tutor.router, prefix="/course_by_tutor", tags=["Course by Tutor"])

# Course By subject
# from coursebysubject import course_by_subject
# app.include_router(course_by_subject.router, prefix="/course_by_subject", tags=["Course by Subject"])

# # Extensive Course
from courses_extensive import extensive_course
app.include_router(extensive_course.router, prefix="/extensive_course", tags=["Extensive Course"])

# # Micro Course
# from courses_micro import micro_course
# app.include_router(micro_course.router, prefix="/micro_course", tags=["Micro Course"])

# # Master Course
from courses_master import master_course
app.include_router(master_course.router, prefix="/master_course", tags=["master Course"])

#image upload
import uuid
from pathlib import Path

import os
from os.path import dirname, abspath, join
import shutil
import aiofiles

app.mount("/static", StaticFiles(directory="static"), name="static")
dirname = dirname(dirname(abspath(__file__)))
images_path = join(dirname, '/static')
 
@app.post("/cv2")
async def get_image(request: Request, file: UploadFile = File(...)):
 
    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not extension:
        return "Image must be jpg or png format!"
    # async with aiofiles.open('filename', mode='r') as f:
    #     contents = await f.read()

    
    # outputImage = Image.fromarray(sr_img)  
    suffix = Path(file.filename).suffix
    filename = time.strftime( str(uuid.uuid4().hex) + "%Y%m%d-%H%M%S" + suffix )
    
    with open("static/"+filename, "wb") as image:
        shutil.copyfileobj(file.file, image)

    #url = str("media/"+file.filename)
    file_path = os.path.join(images_path, filename)
    print(file_path)
    client_host = request.client.host
    return {"url": file_path,"client_host": client_host}

    