from api.models import NoteSchema
#from app.db import notes, database
from configs.connection import database, extensive_course


async def post(payload: NoteSchema):
    query = extensive_course.insert().values(Name=payload.Name, title=payload.title, description=payload.description)
    return await database.execute(query=query)

async def get(id: int):
    query = extensive_course.select().where(id == extensive_course.c.id)
    return await database.fetch_one(query=query)

async def get_all():
    query = extensive_course.select()
    return await database.fetch_all(query=query)

async def put(id: int, payload: NoteSchema):
    query = (extensive_course.update().where(id == extensive_course.c.id).values(Name=payload.Name,title=payload.title, description=payload.description).returning(extensive_course.c.id))
    return await database.execute(query=query)



async def delete(id: int):
    query = extensive_course.delete().where(id == extensive_course.c.id)
    return await database.execute(query=query)