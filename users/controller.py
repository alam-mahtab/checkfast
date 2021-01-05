from fastapi import APIRouter, Depends
from auth import model
from utils import util
from configs.connection import database
# Pagination
from fastapi_pagination import Page, pagination_params
from fastapi_pagination.paginator import paginate

router = APIRouter()

@router.get("/users/me", response_model = model.UserList)
async def read_user_me(currentuser: model.UserList = Depends(util.get_current_active_user)):
    return currentuser

@router.get("/users",response_model=Page[model.UserList],dependencies=[Depends(pagination_params)])
async def find_all_user(
    currentuser : model.UserList = Depends(util.get_current_active_user),
):
    query = "select * from users"
    user_all = await database.fetch_all(query=query, values={}) 
    return paginate(user_all)