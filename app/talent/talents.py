from typing import List
from fastapi import Depends,File, UploadFile, APIRouter
from sqlalchemy.orm import Session
from . import crud, models
from .database import SessionLocal, engine
from .schemas import TalentBase, TalentList
from .models import Talent
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

import uuid
from pathlib import Path
import time
#from fastapi.staticfiles import StaticFiles
from starlette.staticfiles import StaticFiles
import os
from os.path import dirname, abspath, join
import shutil

router.mount("/static", StaticFiles(directory="static"), name="static")
dirname = dirname(dirname(abspath(__file__)))
images_path = join(dirname, '/static')

# router.mount("/app", StaticFiles(directory="app"), name="app")
# # dirname = dirname(dirname(abspath(__file__)))
# # images_path = join(dirname, '/static')

# current_file = Path(__file__)
# current_file_dir = current_file.parent
# project_root = current_file_dir.parent
# project_root_absolute = project_root.resolve()
# static_root_absolute = project_root_absolute / "static" 

@router.post("/talent/")
def create_talent(
    desc:str,name:str,type:str,status:int,file_pro: UploadFile= File(...), file_cover: UploadFile= File(...), db: Session = Depends(get_db)
):

    extension_pro = file_pro.filename.split(".")[-1] in ("jpg", "jpeg", "png") 
    if not extension_pro:
        return "Image must be jpg or png format!"
    suffix_pro = Path(file_pro.filename).suffix
    filename_pro = time.strftime( str(uuid.uuid4().hex) + "%Y%m%d-%H%M%S" + suffix_pro )
    with open("static/"+filename_pro, "wb") as image:
        shutil.copyfileobj(file_pro.file, image)
    url_profile = os.path.join(images_path, filename_pro)

    extension_cover = file_cover.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not extension_cover:
        return "Image must be jpg or png format!"
    suffix_cover =Path(file_cover.filename).suffix
    filename_cover = time.strftime( str(uuid.uuid4().hex) + "%Y%m%d-%H%M%S" + suffix_cover )
    with open("static/"+filename_cover, "wb") as image:
        shutil.copyfileobj(file_cover.file, image)
    url_cover = os.path.join(images_path, filename_cover)

    return crud.create_talent(db=db,name=name,desc=desc,url_profile=url_profile,url_cover=url_cover,type=type,status=status)


@router.get("/talents/" ,dependencies=[Depends(pagination_params)])
def talent_list(db: Session = Depends(get_db)):
    talent_all =crud.talent_list(db=db)
    return paginate(talent_all)

@router.get("/talents/{talent_id}")
def talent_detail(talent_id:int,db: Session = Depends(get_db)):
    return crud.get_talent(db=db, id=talent_id)

@router.delete("/talents/{talent_id}")
async def delete(talent_id: int, db: Session = Depends(get_db)):
    deleted = await crud.delete(db, talent_id)
    return {"deleted": deleted}

# 1.Writer
@router.get("/Witer/" ,dependencies=[Depends(pagination_params)])
def writer_list(db: Session = Depends(get_db)):
    writer_all =crud.writer_list(db=db)
    return paginate(writer_all)
# 2.Director
@router.get("/Director/" ,dependencies=[Depends(pagination_params)])
def director_list(db: Session = Depends(get_db)):
    director_all =crud.director_list(db=db)
    return paginate(director_all)
# 3.Actor
@router.get("/Actor/" ,dependencies=[Depends(pagination_params)])
def actor_list(db: Session = Depends(get_db)):
    actor_all =crud.actor_list(db=db)
    return paginate(actor_all)
# 4.Cinematographer
@router.get("/Cinematographer/" ,dependencies=[Depends(pagination_params)])
def cinematographer_list(db: Session = Depends(get_db)):
    cinematographer_all =crud.cinematographer_list(db=db)
    return paginate(cinematographer_all)
# 5.Editor
@router.get("/Editor/" ,dependencies=[Depends(pagination_params)])
def editor_list(db: Session = Depends(get_db)):
    editor_all =crud.editor_list(db=db)
    return paginate(editor_all)
# 6.SoundEditor
@router.get("/Soundeditor/" ,dependencies=[Depends(pagination_params)])
def sound_editor_list(db: Session = Depends(get_db)):
    sound_all =crud.soundeditor_list(db=db)
    return paginate(sound_all)
# 7.Filmmaker
@router.get("/Filmmaker/" ,dependencies=[Depends(pagination_params)])
def filmmaker_list(db: Session = Depends(get_db)):
    filmmaker_all =crud.filmmaker_list(db=db)
    return paginate(filmmaker_all)
# 8.Videographer
@router.get("/Videographer/" ,dependencies=[Depends(pagination_params)])
def videographer_list(db: Session = Depends(get_db)):
    videographer_all =crud.videographer_list(db=db)
    return paginate(videographer_all)
# 9.FilmEditor
@router.get("/Filmediting/" ,dependencies=[Depends(pagination_params)])
def filmediting_list(db: Session = Depends(get_db)):
    filmediting_all =crud.filmediting_list(db=db)
    return paginate(filmediting_all)