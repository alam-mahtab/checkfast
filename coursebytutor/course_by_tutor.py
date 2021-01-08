
from typing import List
from fastapi import Depends,File, UploadFile, APIRouter
from sqlalchemy.orm import Session
from coursebytutor import crud, models
from coursebytutor.database import SessionLocal, engine
import shutil
from coursebytutor.schemas import TutorBase, TutorList
from coursebytutor.models import Tutor
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

models.Base.metadata.create_all(bind=engine)

@router.post("/tutor/")
def create_tutor(
    title:str,desc:str,name:str,file: UploadFile= File(...), db: Session = Depends(get_db)
):

    with open("courseby_tutor_pic/"+file.filename, "wb") as image:
        shutil.copyfileobj(file.file, image)

    url = str("courseby_tutor_pic/"+file.filename)

    return crud.create_tutor(db=db,name=name,title=title,desc=desc,url=url)

@router.get("/tutors/")
def tutor_list(db: Session = Depends(get_db)):
    return crud.tutor_list(db=db)

@router.get("/tutors/{tutor_id}")
def tutor_detail(tutor_id:int,db: Session = Depends(get_db)):
    return crud.get_tutor(db=db, id=tutor_id)