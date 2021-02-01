
from typing import List
from fastapi import Depends,File, UploadFile, APIRouter
from fastapi_pagination.paginator import paginate
from sqlalchemy.orm import Session
from . import crud, models
#from courses_live.database import SessionCourse, some_engine
from writer.database import SessionLocal, engine
import shutil
# Pagination
from fastapi_pagination import Page, pagination_params
from fastapi_pagination.paginator import paginate
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

models.Base.metadata.create_all(bind=engine)

@router.post("/work/")
def create_work(name:str,email:str,message:str,status:int, db: Session = Depends(get_db)):
    return crud.create_work(db=db,status=status,name=name,email=email,message=message)
    

@router.get("/works/" ,dependencies=[Depends(pagination_params)])
def work_list(db: Session = Depends(get_db)):
    work_all = crud.work_list(db=db)
    return paginate(work_all)

@router.get("/works/{work_id}")
def port_detail(work_id:int,db: Session = Depends(get_db)):
    return crud.get_work(db=db, id=work_id)

@router.delete("/works/{work_id}")
async def delete(work_id: int, db: Session = Depends(get_db)):
    deleted = await crud.delete(db, work_id)
    return {"deleted": deleted}