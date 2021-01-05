from api.models import NoteSchema,ImageSchema
#from app.db import notes, database
from configs.connection import database
from api import notes

async def post(payload: ImageSchema):
    query = notes.insert().values(name=payload.file, title=payload.title, description=payload.description, url=payload.url)
    return await database.execute(query=query)
async def get(id: int):
    query = notes.select().where(id == notes.c.id)
    return await database.fetch_one(query=query)

async def get_all():
    query = notes.select()
    return await database.fetch_all(query=query)

async def put(id: int, payload: ImageSchema):
    query = (
        notes
        .update()
        .where(id == notes.c.id)
        .values(title=payload.title, description=payload.description)
        .returning(notes.c.id)
    )
    return await database.execute(query=query)


async def delete(id: int):
    query = notes.delete().where(id == notes.c.id)
    return await database.execute(query=query)
