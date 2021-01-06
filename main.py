from configs.appinfo import setting

from configs.connection import database
from fastapi import FastAPI, Request, Depends

from configs import appinfo
import time
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "http://checkfast.herokuapp.com/docs",
    "https://checkfast.herokuapp.com/docs",
    "uvicorn main:app --host=0.0.0.0 --port=${PORT:-5000}",
    "uvicorn main:app --host=0.0.0.0 --port=${PORT:-5000}/docs",
    "http://0.0.0.0:5000",
    "http://0.0.0.0:5000/docs",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
    "http://localhost:4200",
    "http://localhost:5000",
    "http://127.0.0.1:5000",
    "http://127.0.0.1:4200",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["DELETE", "GET", "POST", "PUT"],
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
from api import notes, ping, imgnotes
app.include_router(ping.router)
app.include_router(notes.router, prefix="/notes", tags=["notes"])
app.include_router(imgnotes.router, prefix="/imgnotes", tags=["imgnotes"])

# For Comments
from comment import comnotes
app.include_router(comnotes.router, prefix="/comnotes", tags=["Comment"])

# For Feeds
from feed import fnotes
app.include_router(fnotes.router, prefix="/fnotes", tags=["Feed"])