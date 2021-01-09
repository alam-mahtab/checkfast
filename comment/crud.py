from comment.models import CommentSchema
#from app.db import notes, database
from configs.connection import database, comnotes


async def post(payload: CommentSchema):
    query = comnotes.insert().values(Name=payload.Name,title=payload.title, description=payload.description)
    return await database.execute(query=query)

async def get(id: int):
    query = comnotes.select().where(id == comnotes.c.id)
    return await database.fetch_one(query=query)

async def get_all():
    query = comnotes.select()
    return await database.fetch_all(query=query)

async def put(id: int, payload: CommentSchema):
    query = (
        comnotes
        .update()
        .where(id == comnotes.c.id)
        .values(Name=payload.Name,title=payload.title,description=payload.description)
        .returning(comnotes.c.id)
    )
    return await database.execute(query=query)



async def delete(id: int):
    query = comnotes.delete().where(id == comnotes.c.id)
    return await database.execute(query=query)