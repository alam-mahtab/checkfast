from typing import List

from api import crud
from api.models import NoteDB, NoteSchema
from fastapi import APIRouter, HTTPException, Path, Depends
from fastapi import FastAPI, File, Form, UploadFile
# pagination
from fastapi_pagination import Page, pagination_params
from fastapi_pagination.paginator import paginate

router = APIRouter()


@router.post("/", response_model=NoteDB, status_code=201)
async def create_extensive_course(payload: NoteSchema):
    extensive_course_id = await crud.post(payload)

    response_object = {
        "id": extensive_course_id,
        "Name": payload.Name,
        "title": payload.title,
        "description": payload.description,
    }
    return response_object


@router.get("/{id}/", response_model=NoteDB)
async def read_extensive_course(id: int = Path(..., gt=0),):
    e_c = await crud.get(id)
    if not e_c:
        raise HTTPException(status_code=404, detail="extensive_course not found")
    return e_c


@router.get("/", response_model=Page[NoteDB], dependencies=[Depends(pagination_params)])
async def read_all_extensive_course():
    extensive_course_all = await crud.get_all()
    return paginate(extensive_course_all)

@router.put("/{id}/", response_model=NoteDB)
async def update_extensive_course(payload: NoteSchema, id: int = Path(..., gt=0),):
    e_c = await crud.get(id)
    if not e_c:
        raise HTTPException(status_code=404, detail="extensive_course not found")
    
    extensive_course_id = await crud.put(id, payload)

    response_object = {
        "id": extensive_course_id,
        "Name": payload.Name,
        "title": payload.title,
        "description": payload.description,
    }
    return response_object


@router.delete("/{id}/", response_model=NoteDB)
async def delete_extensive_course(id: int = Path(..., gt=0)):
    e_c = await crud.get(id)
    if not e_c:
        raise HTTPException(status_code=404, detail="extensive_course not found")

    await crud.delete(id)

    return e_c

