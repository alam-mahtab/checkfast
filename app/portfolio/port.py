
from typing import List
from fastapi import Depends,File, UploadFile, APIRouter, HTTPException
from fastapi_pagination.paginator import paginate
from sqlalchemy.orm import Session
from . import crud, models
#from courses_live.database import SessionCourse, some_engine
from app.talent.database import SessionLocal, engine
import shutil
# Pagination
from fastapi_pagination import Page, pagination_params
from fastapi_pagination.paginator import paginate
router = APIRouter()


import uuid
from pathlib import Path
import time
#from fastapi.staticfiles import StaticFiles
from starlette.staticfiles import StaticFiles
import os
from os.path import dirname, abspath, join


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

models.Base.metadata.create_all(bind=engine)
router.mount("/static", StaticFiles(directory="static"), name="static")
dirname = dirname(dirname(abspath(__file__)))
images_path = join(dirname, '/static')

# # router.mount("/static", StaticFiles(directory="static"), name="static")
# # dirname = dirname(dirname(abspath(__file__)))
# # images_path = join(dirname, '/static')

# current_file = Path(__file__)
# current_file_dir = current_file.parent
# project_root = current_file_dir.parent
# project_root_absolute = project_root.resolve()
# static_root_absolute = project_root_absolute / "static" 

@router.post("/port/")
def create_port(status:int,file: UploadFile= File(...), db: Session = Depends(get_db)):

    # extension = file.filename.split(".")[-1] in ("mp4", "3gp")
    # if not extension:
    #     return "video must be mp4 or 3gp format!"
    
    # outputImage = Image.fromarray(sr_img)  
    suffix = Path(file.filename).suffix
    filename = time.strftime( str(uuid.uuid4().hex) + "%Y%m%d-%H%M%S" + suffix )
    with open("static/"+filename, "wb") as video:
        shutil.copyfileobj(file.file, video)

    #url = str("media/"+file.filename)
    url = os.path.join(images_path, filename)
    crud.create_port(db=db,status=status,url=url)
    return {"url": url,"status":status}
@router.put("/port/{id}")
def update_port(id:int,status:int,file: UploadFile= File(...), db: Session = Depends(get_db)):

    # extension = file.filename.split(".")[-1] in ("mp4", "3gp")
    # if not extension:
    #     return "video must be mp4 or 3gp format!"
    
    # outputImage = Image.fromarray(sr_img)  
    suffix = Path(file.filename).suffix
    filename = time.strftime( str(uuid.uuid4().hex) + "%Y%m%d-%H%M%S" + suffix )
    with open("static/"+filename, "wb") as video:
        shutil.copyfileobj(file.file, video)

    #url = str("media/"+file.filename)
    url = os.path.join(images_path, filename)
    subject =  crud.get_port(db,id)
    if not subject:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    query = "UPDATE ports SET status='"+str(status)+"', url='"+str(url)+"' WHERE id='"+str(id)+"'"
    db.execute(query)
    db.commit()
    return {"Result" : "Filmography Updated Succesfully"}
@router.get("/ports/" ,dependencies=[Depends(pagination_params)])
def port_list(db: Session = Depends(get_db)):
    port_all = crud.port_list(db=db)
    return paginate(port_all)

@router.get("/ports/{port_id}")
def port_detail(port_id:int,db: Session = Depends(get_db)):
    return crud.get_port(db=db, id=port_id)

@router.delete("/ports/{port_id}")
async def delete(port_id: int, db: Session = Depends(get_db)):
    deleted = await crud.delete(db, port_id)
    return {"deleted": deleted}


# Writer
@router.get("/writer/" ,dependencies=[Depends(pagination_params)])
def portfolio_writer_list(db: Session = Depends(get_db)):
    portfolio_writer_all = crud.portfolio_writer_list(db=db)
    return paginate(portfolio_writer_all)
# Director
@router.get("/director/" ,dependencies=[Depends(pagination_params)])
def portfolio_director_list(db: Session = Depends(get_db)):
    portfolio_director_all = crud.portfolio_director_list(db=db)
    return paginate(portfolio_director_all)
# Actor
@router.get("/actor/" ,dependencies=[Depends(pagination_params)])
def portfolio_actor_list(db: Session = Depends(get_db)):
    portfolio_actor_all = crud.portfolio_actor_list(db=db)
    return paginate(portfolio_actor_all)
# Cinematographer
@router.get("/cinematographer/" ,dependencies=[Depends(pagination_params)])
def portfolio_cinematographer_list(db: Session = Depends(get_db)):
    portfolio_cinematographer_all = crud.portfolio_cinematographer_list(db=db)
    return paginate(portfolio_cinematographer_all)
# Editor
@router.get("/editor/" ,dependencies=[Depends(pagination_params)])
def portfolio_editor_list(db: Session = Depends(get_db)):
    portfolio_editor_all = crud.portfolio_editor_list(db=db)
    return paginate(portfolio_editor_all)
# SoundEditor
@router.get("/sound_editor/" ,dependencies=[Depends(pagination_params)])
def portfolio_sound_editor_list(db: Session = Depends(get_db)):
    portfolio_sound_all = crud.portfolio_sound_editor_list(db=db)
    return paginate(portfolio_sound_all)
# Film_maker
@router.get("/film_maker/" ,dependencies=[Depends(pagination_params)])
def portfolio_film_maker_list(db: Session = Depends(get_db)):
    portfolio_film_maker_all = crud.portfolio_filmediting_list(db=db)
    return paginate(portfolio_film_maker_all)
# Videographer
@router.get("/video_grapher/" ,dependencies=[Depends(pagination_params)])
def portfolio_video_grapher_list(db: Session = Depends(get_db)):
    portfolio_video_grapher_all = crud.portfolio_videographer_list(db=db)
    return paginate(portfolio_video_grapher_all)
# FilmEditing
@router.get("/film_editing/" ,dependencies=[Depends(pagination_params)])
def portfolio_film_editing_list(db: Session = Depends(get_db)):
    portfolio_film_editing_all = crud.portfolio_filmediting_list(db=db)
    return paginate(portfolio_film_editing_all)