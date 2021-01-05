from typing import List

from comment import crud
from comment.models import CommentDB, CommentSchema
from fastapi import APIRouter, HTTPException, Path
from fastapi import FastAPI, File, Form, UploadFile

router = APIRouter()


@router.post("/", response_model=CommentDB, status_code=201)
async def create_comment(payload: CommentSchema):
    comment_id = await crud.post(payload)

    response_object = {
        "id": comment_id,
        "title": payload.title,
        "description": payload.description,
    }
    return response_object


@router.get("/{id}/", response_model=CommentDB)
async def read_comment(id: int = Path(..., gt=0),):
    comment = await crud.get(id)
    if not comment:
        raise HTTPException(status_code=404, detail="comment not found")
    return comment


@router.get("/", response_model=List[CommentDB])
async def read_all_comments():
    return await crud.get_all()


@router.put("/{id}/", response_model=CommentDB)
async def update_comment(payload: CommentSchema, id: int = Path(..., gt=0),):
    comment = await crud.get(id)
    if not comment:
        raise HTTPException(status_code=404, detail="comment not found")

    comment_id = await crud.put(id, payload)

    response_object = {
        "id": comment_id,
        "title": payload.title,
        "description": payload.description,
    }
    return response_object


@router.delete("/{id}/", response_model=CommentDB)
async def delete_comment(id: int = Path(..., gt=0)):
    comment = await crud.get(id)
    if not comment:
        raise HTTPException(status_code=404, detail="comment not found")

    await crud.delete(id)

    return comment

