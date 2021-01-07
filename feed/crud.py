from feed.models import FeedSchema
#from app.db import notes, database
from configs.connection import database, fnotes


async def post(payload: FeedSchema):
    query = fnotes.insert().values(Name=payload.Name, title=payload.title, description=payload.description)
    return await database.execute(query=query)

async def get(id: int):
    query = fnotes.select().where(id == fnotes.c.id)
    return await database.fetch_one(query=query)

async def get_all():
    query = fnotes.select()
    return await database.fetch_all(query=query)

async def put(id: int, payload: FeedSchema):
    query = (
        fnotes
        .update()
        .where(id == fnotes.c.id)
        .values(Name=payload.Name, title=payload.title, description=payload.description)
        .returning(fnotes.c.id)
    )
    return await database.execute(query=query)



async def delete(id: int):
    query = fnotes.delete().where(id == fnotes.c.id)
    return await database.execute(query=query)