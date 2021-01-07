from api.models import NoteSchema,ImageSchema
#from app.db import notes, database
from configs.connection import database
from api import extensive_course

async def post(payload: ImageSchema):
    query = extensive_course.insert().values(name=payload.file, title=payload.title, description=payload.description, url=payload.url)
    return await database.execute(query=query)
async def get(id: int):
    query = extensive_course.select().where(id == extensive_course.c.id)
    return await database.fetch_one(query=query)

async def get_all():
    query = extensive_course.select()
    return await database.fetch_all(query=query)

async def put(id: int, payload: ImageSchema):
    query = (
        extensive_course
        .update()
        .where(id == extensive_course.c.id)
        .values(title=payload.title, description=payload.description)
        .returning(extensive_course.c.id)
    )
    return await database.execute(query=query)


async def delete(id: int):
    query = extensive_course.delete().where(id == extensive_course.c.id)
    return await database.execute(query=query)
