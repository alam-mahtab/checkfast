
from typing import List
from fastapi import Depends,File, UploadFile, APIRouter
from fastapi_pagination.paginator import paginate
from sqlalchemy.orm import Session
from app.awards import crud, models
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
from fastapi.staticfiles import StaticFiles
#from starlette.staticfiles import StaticFiles
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

# router.mount("/static", StaticFiles(directory="static"), name="static")
# dirname = dirname(dirname(abspath(__file__)))
# images_path = join(dirname, 'static')

# current_file = Path(__file__)
# current_file_dir = current_file.parent
# project_root = current_file_dir.parent
# project_root_absolute = project_root.resolve()
# static_root_absolute = project_root_absolute / "static" 

@router.post("/award/")
def create_award(
    title:str,desc:str,status:int,file: UploadFile= File(...), db: Session = Depends(get_db)
):

    extension = file.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not extension:
        return "Image must be jpg or png format!"
    # print(current_file)
    # print(project_root)
    # print(current_file_dir)
    # print(project_root_absolute)
    # print("hello")
    # print(dirname)
    # print(images_path)
    # outputImage = Image.fromarray(sr_img)  
    suffix = Path(file.filename).suffix
    filename = time.strftime( str(uuid.uuid4().hex) + "%Y%m%d-%H%M%S" + suffix )
    #print(filename)
    with open("static/"+filename, "wb") as image:
        shutil.copyfileobj(file.file, image)

    #url = str("media/"+file.filename)
    #print(static_root_absolute)
    url = os.path.join(images_path, filename)
    return crud.create_award(db=db,status=status,title=title,desc=desc,url=url)

@router.get("/Award/" ,dependencies=[Depends(pagination_params)])
def award_list(db: Session = Depends(get_db)):
    award_all = crud.award_list(db=db)
    return paginate(award_all)

@router.get("/Award/{award_id}")
def award_detail(award_id:int,db: Session = Depends(get_db)):
    return crud.get_award(db=db, id=award_id)

@router.delete("/Award/{award_id}")
async def delete(award_id: int, db: Session = Depends(get_db)):
    deleted = await crud.delete(db, award_id)
    return {"deleted": deleted}


# Writer
@router.get("/writer/" ,dependencies=[Depends(pagination_params)])
def Award_writer_list(db: Session = Depends(get_db)):
    writer_all = crud.Award_writer_list(db=db)
    return paginate(writer_all)

# Director
@router.get("/director/" ,dependencies=[Depends(pagination_params)])
def Award_director_list(db: Session = Depends(get_db)):
    director_all = crud.Award_director_list(db=db)
    return paginate(director_all)
# Actor
@router.get("/actor/" ,dependencies=[Depends(pagination_params)])
def Award_actor_list(db: Session = Depends(get_db)):
    actor_all = crud.Award_actor_list(db=db)
    return paginate(actor_all)
# Cinematographer
@router.get("/cinematographer/" ,dependencies=[Depends(pagination_params)])
def Award_cinematographer_list(db: Session = Depends(get_db)):
    cinematographer_all = crud.Award_cinematographer_list(db=db)
    return paginate(cinematographer_all)
# Editor
@router.get("/editor/" ,dependencies=[Depends(pagination_params)])
def Award_editor_list(db: Session = Depends(get_db)):
    editor_all = crud.Award_editor_list(db=db)
    return paginate(editor_all)
# SoundEditor
@router.get("/sound_editor/" ,dependencies=[Depends(pagination_params)])
def Award_sound_editor_list(db: Session = Depends(get_db)):
    sound_all = crud.Award_sound_editor_list(db=db)
    return paginate(sound_all)
# Film_maker
@router.get("/film_maker/" ,dependencies=[Depends(pagination_params)])
def Award_film_maker_list(db: Session = Depends(get_db)):
    film_maker_all = crud.Award_filmmaker_list(db=db)
    return paginate(film_maker_all)
# Videographer
@router.get("/video_grapher/" ,dependencies=[Depends(pagination_params)])
def Award_video_grapher_list(db: Session = Depends(get_db)):
    video_grapher_all = crud.Award_videographer_list(db=db)
    return paginate(video_grapher_all)
# FilmEditing
@router.get("/film_editing/" ,dependencies=[Depends(pagination_params)])
def Award_film_editing_list(db: Session = Depends(get_db)):
    film_editing_all = crud.Award_filmediting_list(db=db)
    return paginate(film_editing_all)