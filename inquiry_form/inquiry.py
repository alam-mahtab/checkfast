from typing import Dict, List
from fastapi import Depends,File, UploadFile, APIRouter, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
#from courses_live.database import SessionCourse, some_engine
from talent.database import SessionLocal, engine
#from coursebysubject.models import subjects
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

@router.post("/inquiry/")
def create_inquiry(
    title:str,desc:str,name:str,email:str,interview:bool=False,work_or_commision:bool=False,other:bool=False, db: Session = Depends(get_db)
):
    return crud.create_inquiry(db=db,name=name,title=title,desc=desc,email=email,interview=interview,work_or_commision=work_or_commision,other=other)

@router.get("/Inquiries/"  ,dependencies=[Depends(pagination_params)])
def inquiry_list(db: Session = Depends(get_db)):
    inquiry_all = crud.inquiry_list(db=db)
    return paginate(inquiry_all)

@router.get("/inquiries/{inquiry_id}")
def free_detail(inquiry_id:int,db: Session = Depends(get_db)):
    return crud.get_inquiry(db=db, id=inquiry_id)

@router.delete("/inquiries/{inquiry_id}")
async def delete(inquiry_id: int, db: Session = Depends(get_db)):
    deleted = await crud.delete(db, inquiry_id)
    return {"deleted": deleted}
