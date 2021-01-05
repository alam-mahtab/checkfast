from configs.appinfo import setting

from configs.connection import database
from fastapi import FastAPI, Request, Depends
from functools import lru_cache
from configs import appinfo
import time


app = FastAPI(debug=True)



@lru_cache()
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