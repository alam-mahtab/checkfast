from typing import List

from feed import crud
from feed.models import FeedDB, FeedSchema
from fastapi import APIRouter, HTTPException, Path
from fastapi import FastAPI, File, Form, UploadFile
# Pagination
from fastapi_pagination import Page, PaginationParams
from fastapi_pagination.ext.sqlalchemy import paginate


router = APIRouter()


@router.post("/", response_model=FeedDB, status_code=201)
async def create_note(payload: FeedSchema):
    fnote_id = await crud.post(payload)

    response_object = {
        "id": fnote_id,
        "title": payload.title,
        "description": payload.description,
    }
    return response_object


@router.get("/{id}/", response_model=FeedDB)
async def read_note(id: int = Path(..., gt=0),):
    fnote = await crud.get(id)
    if not fnote:
        raise HTTPException(status_code=404, detail="Feed not found")
    return fnote


@router.get("/", response_model=Page[FeedDB])
async def read_all_fnotes():
    return await crud.get_all()


@router.put("/{id}/", response_model=FeedDB)
async def update_note(payload: FeedSchema, id: int = Path(..., gt=0),):
    fnote = await crud.get(id)
    if not fnote:
        raise HTTPException(status_code=404, detail="Feed not found")

    fnote_id = await crud.put(id, payload)

    response_object = {
        "id": fnote_id,
        "title": payload.title,
        "description": payload.description,
    }
    return response_object


@router.delete("/{id}/", response_model=FeedDB)
async def delete_note(id: int = Path(..., gt=0)):
    fnote = await crud.get(id)
    if not fnote:
        raise HTTPException(status_code=404, detail="Note not found")

    await crud.delete(id)

    return fnote

