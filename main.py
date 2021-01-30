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

tags_metadata = [
    {   "name": "Auth",
        "description": "Operations with authentication. The **login** logic is also here.", },
    {   "name": "Awards",
        "description": "Operations with awards section in talent & courses. sorting done by status",},
    {   "name": "Filmography",
        "description": "Operations with filmography section in talent & courses. sorting done by status",    },
    {   "name": "Portfolio",
        "description": "Operations with portfolio section in talent & courses. sorting done by status",    },
    {   "name": "Users",
        "description": "Manage users. So _fancy_ they have their own docs.",
        # "externalDocs": {
        #     "description": "Items external docs",
        #     "url": "https://fastapi.tiangolo.com/",
        # },
    },
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

# For Inquiry
from inquiry_form import inquiry
app.include_router(inquiry.router, prefix="/inquiry", tags=["Inquiry"])

# For FAQS
from Faqs import question
app.include_router(question.router, prefix="/faq", tags=["FAQS"])

# For Awards
from awards import award
app.include_router(award.router, prefix="/award", tags=["Awards"])

# For Filmography
from filmography import filmo
app.include_router(filmo.router, prefix="/filmo", tags=["Filmography"])

# For Portfolio
from portfolio import port
app.include_router(port.router, prefix="/port", tags=["Portfolio"])

#For live course
from courses_live import live_course
app.include_router(live_course.router, prefix="/live_course", tags=["Live Course"])

# Course By tutor
from coursebytutor import course_by_tutor
app.include_router(course_by_tutor.router, prefix="/course_by_tutor", tags=["Course by Tutor"])

# Course By subject
from coursebysubject import course_by_subject
app.include_router(course_by_subject.router, prefix="/course_by_subject", tags=["Course by Subject"])

# # Extensive Course
from courses_extensive import extensive_course
app.include_router(extensive_course.router, prefix="/extensive_course", tags=["Extensive Course"])

# # Micro Course
from courses_micro import micro_course
app.include_router(micro_course.router, prefix="/micro_course", tags=["Micro Course"])

# # Master Course
from courses_master import master_course
app.include_router(master_course.router, prefix="/master_course", tags=["Master Course"])

# # Free Course
from freecourse import course_free
app.include_router(course_free.router, prefix="/course_free", tags=["Free Course"])

# # writer
from writer import writer_skill
app.include_router(writer_skill.router, prefix="/writer", tags=["Writer"])

# # actor
from actor import actor_skill
app.include_router(actor_skill.router, prefix="/actor", tags=["Actor"])

# # cinematographer
from cinematographer import cinematographer_skill
app.include_router(cinematographer_skill.router, prefix="/cinematographer", tags=["Cinematographer"])

# # director
from director import director_skill
app.include_router(director_skill.router, prefix="/director", tags=["Director"])

# # editor
from editor import editor_skill
app.include_router(editor_skill.router, prefix="/editor", tags=["Editor"])

# # film_editing
from film_editing import film_edit_skill
app.include_router(film_edit_skill.router, prefix="/film_editing", tags=["Film Editor"])

# # film_maker
from filmmaker import film_maker_skill
app.include_router(film_maker_skill.router, prefix="/film_maker", tags=["Film Maker"])

# # sound_editor
from sound_editor import sound_editor_skill
app.include_router(sound_editor_skill.router, prefix="/sound_editor", tags=["Sound Editor"])

# # videographer
from vidographer import videographer_skill
app.include_router(videographer_skill.router, prefix="/videographer", tags=["Videographer"])

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
 
   # extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    #if not extension:
     #   return "Image must be jpg or png format!"  
    suffix = Path(file.filename).suffix
    filename = time.strftime( str(uuid.uuid4().hex) + "%Y%m%d-%H%M%S" + suffix )
    
    with open("static/"+filename, "wb") as image:
        shutil.copyfileobj(file.file, image)

    #url = str("media/"+file.filename)
    file_path = os.path.join(images_path, filename)
    print(file_path)
    client_host = request.client.host
    return {"url": file_path,"client_host": client_host}

from fastapi.responses import StreamingResponse

some_file_path = "C:\\Users\\Ehtesham Hassan\\Desktop\\Testfast\\8.mp4" #os.path.join(UPLOAD_FOLDER, "1.mp4")

@app.get("/video")
def video():
    file_like = open(some_file_path, mode="rb")
    
    return StreamingResponse(file_like, media_type="video/mp4")

async def fake_video_streamer():
    for i in range(10000):
        yield b"some fake video bytes"


@app.get("/stream")
async def stream():
    return StreamingResponse(fake_video_streamer())

# Send mail
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from pydantic import EmailStr
from pydantic import EmailStr, BaseModel
from starlette.responses import JSONResponse
from typing import List
class EmailSchema(BaseModel):
    email: List[EmailStr]


conf = ConnectionConfig(
    MAIL_USERNAME = "priyanka@mobirizer.com",
    MAIL_PASSWORD = "123456789",
    MAIL_FROM = "priyanka@mobirizer.com",
    MAIL_PORT = 587,  
    MAIL_SERVER = "smtpout.secureserver.net",
    MAIL_TLS = True,
    MAIL_SSL = False,
    USE_CREDENTIALS = True
)



html = """
<p>Hi this test mail using BackgroundTasks, thanks for using Fastapi-mail</p> 
"""


@app.post("/email")
async def simple_send(email: EmailSchema) -> JSONResponse:

    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=email.dict().get("email"),  # List of recipients, as many as you can pass 
        body=html,
        subtype="html"
        )

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})    
    