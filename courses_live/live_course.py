
from typing import List
from fastapi import Depends,File, UploadFile, APIRouter
from sqlalchemy.orm import Session
from courses_live import crud, models
from courses_live.database import SessionLocal, engine
import shutil
from courses_live.schemas import LiveBase, LiveList
from courses_live.models import Live
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

models.Base.metadata.create_all(bind=engine)

@router.post("/live/")
def create_live(
    title:str,desc:str,name:str,file: UploadFile= File(...), db: Session = Depends(get_db)
):

    with open("live_course_pic/"+file.filename, "wb") as image:
        shutil.copyfileobj(file.file, image)

    url = str("live_course_pic/"+file.filename)

    return crud.create_live(db=db,name=name,title=title,desc=desc,url=url)

@router.get("/lives/")
def live_list(db: Session = Depends(get_db)):
    return crud.live_list(db=db)

@router.get("/lives/{live_id}")
def live_detail(live_id:int,db: Session = Depends(get_db)):
    return crud.get_live(db=db, id=live_id)