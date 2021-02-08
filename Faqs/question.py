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

@router.post("/faq/")
def create_faq(question:str, answer:str, db: Session = Depends(get_db)
):
    return crud.create_faq(db=db,question=question,answer=answer)

@router.get("/faqs/"  ,dependencies=[Depends(pagination_params)])
def faq_list(db: Session = Depends(get_db)):
    faq_all = crud.faq_list(db=db)
    return paginate(faq_all)

@router.get("/faqs/{faq_id}")
def faq_detail(faq_id:int,db: Session = Depends(get_db)):
    return crud.get_faq(db=db, id=faq_id)

@router.delete("/faqs/{faq_id}")
async def delete(faq_id: int, db: Session = Depends(get_db)):
    deleted = await crud.delete(db, faq_id)
    return {"deleted": deleted}
