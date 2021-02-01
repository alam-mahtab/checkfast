from fastapi import APIRouter, Depends
from auth import model
from utils import util
from configs.connection import database
# Pagination
from fastapi_pagination import Page, pagination_params
from fastapi_pagination.paginator import paginate
from db.table import Users
router = APIRouter()

@router.get("/users/me", response_model = model.UserList)
async def read_user_me(currentuser: model.UserList = Depends(util.get_current_active_user)):
    return currentuser

@router.get("/users/{userId}", response_model=model.UserList)
async def find_user_by_id(user : model.UserList):
    query = Users.select().where(Users.c.id == user.id)
    return await database.fetch_one(query)
    
@router.delete("/users/{userId}")
async def delete_user(user : model.UserDelete):
    query = Users.delete().where(Users.c.id == user.id)
    await database.execute(query=query)

    return {
        "status" : True,
        "message" : "This User Is been Delete"
    }


@router.get("/users",response_model=Page[model.UserList],dependencies=[Depends(pagination_params)])
async def find_all_user(
    currentuser : model.UserList = Depends(util.get_current_active_user),
):
    query = "select * from Users"
    user_all = await database.fetch_all(query=query, values={}) 
    return paginate(user_all)