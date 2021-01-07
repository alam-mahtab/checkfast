from fastapi import FastAPI, File, Form, UploadFile, APIRouter, HTTPException, Path
from typing import List

from api import imagecrud
from api.models import ImageDB,ImageSchema

router = APIRouter()

@router.post("/",response_model=ImageDB, status_code=201)
async def create_file(payload: ImageSchema,
    file = File(...), token: str = Form(...)):
    imgnote_id = await imagecrud.post(payload)
    response_object = {
        "id": imgnote_id,
        "title": payload.title,
        "description": payload.description,
        }

    return response_object + {"file_size": len(file),
        "token": token,
        "fileb_content_type": file.content_type,}