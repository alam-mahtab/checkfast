# from typing import Dict, List
# from fastapi import Depends,File, UploadFile, APIRouter, HTTPException
# from sqlalchemy.orm import Session
# from . import crud, schemas
# from app.authentication import models
# from app.talent.database import SessionLocal, engine,database
# import shutil
# import datetime
# from fastapi_pagination import Page, pagination_params
# from fastapi_pagination.paginator import paginate
# router = APIRouter()


# import uuid
# from pathlib import Path
# import time
# #from fastapi.staticfiles import StaticFiles
# from starlette.staticfiles import StaticFiles
# import os
# from os.path import dirname, abspath, join


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# models.Base.metadata.create_all(bind=engine)

# @router.post("/courses/{courses_id}/comment")
# def create_comment(name:str,email:str,body:str,courses_id:int,db:Session=Depends(get_db)):
#     return crud.create_comment(db=db,name=name,email=email,body=body,courses_id=courses_id)