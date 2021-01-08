from typing import List
from fastapi import Depends, FastAPI, HTTPException, status,File, UploadFile, APIRouter
from sqlalchemy.orm import Session

from app1 import crud, models
from app1.database import SessionLocal, engine
import shutil
from app1.schemas import PostBase, PostList
from app1.models import Post
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

models.Base.metadata.create_all(bind=engine)

@router.post("/posts/")
def create_post(
    title:str,desc:str,name:str,file: UploadFile = File(...), db: Session = Depends(get_db)
):

    with open("media/"+file.filename, "wb") as image:
        shutil.copyfileobj(file.file, image)

    url = str("media/"+file.filename)

    return crud.create_post(db=db,name=name,title=title,desc=desc,url=url)

@router.get("/posts/")
def post_list(db: Session = Depends(get_db)):
    return crud.post_list(db=db)

@router.get("/posts/{post_id}")
def post_detail(post_id:int,db: Session = Depends(get_db)):
    return crud.get_post(db=db, id=post_id)