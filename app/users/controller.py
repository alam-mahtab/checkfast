from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.sql.functions import user
from sqlalchemy.orm import Session
from app.authentication import schemas, models
from app.utils import util
from app.All_Course import crud
from app.talent.database import database, SessionLocal, engine
# Pagination
from fastapi_pagination import Page, pagination_params
from fastapi_pagination.paginator import paginate
from app.authentication.models import Users
router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

models.Base.metadata.create_all(bind=engine)
@router.get("/users/me", response_model = schemas.UserList)
async def read_user_me(currentuser: schemas.UserList = Depends(util.get_current_active_user)):
    return currentuser

@router.get("/users/username", response_model= schemas.UserList)
async def find_user_by_username(username : str):
    query = Users.__table__.select().where(Users.username == username)
    return await database.fetch_one(query)

@router.get("/users/email",response_model = schemas.UserList)
async def find_user_by_email(email : str,currentuser: schemas.UserList = Depends(util.get_current_active_user)):
    query = Users.__table__.select().where(Users.email== email)
    return await database.fetch_one(query)

@router.delete("/users/username")
async def delete_user_by_username(username: str):
    query = Users.__table__.delete().where(Users.username == username)
    await database.execute(query)
    return {
        "status" : True,
        "message" : "This User Is been Delete"
    }

@router.get("/users/{userId}", response_model=schemas.UserList)
async def find_user_by_id(userId: str):
    query = Users.__table__.select().where(Users.id == userId)
    return await database.fetch_one(query)
    
@router.delete("/users/{userId}")
async def delete_user(user : schemas.UserDelete):
    query = Users.__table__.delete().where(Users.id == user.id)
    await database.execute(query=query)

    return {
        "status" : True,
        "message" : "This User Is been Delete"
    }


@router.get("/users",response_model=Page[schemas.UserList],dependencies=[Depends(pagination_params)])
async def find_all_user(
    currentuser : schemas.UserList = Depends(util.get_current_active_user),
):
    query = "select * from Users"
    user_all = await database.fetch_all(query=query, values={}) 
    return paginate(user_all)

@router.post("/users/{userId}/wishlist")
def create_wishlist(client_id:str,course_id:int,db:Session=Depends(get_db)):
    return crud.create_wishlist(db=db,client_id=client_id,course_id=course_id)
@router.get("/users/{userId}/wishlist"  ,dependencies=[Depends(pagination_params)])
def wishlist_list(db: Session = Depends(get_db)):
    wishlist_all = crud.wishlist_list(db=db)
    return paginate(wishlist_all)
@router.get("/users/{userId}/wishlist/{id}")
def comment_detail(id:str,db: Session = Depends(get_db)):
    course_by_id = crud.get_wishlist(db=db, id=id)
    # comments = db.query(models.Comment).filter(models.Comment.courses_id == courses_id)
    #active_comment = comments.filter(models.Comment.is_active == True).all()
    if course_by_id is None:
        raise HTTPException(status_code=404,detail="Comment with this id is not in database")
    return { "Wishlist":course_by_id, }#"active_comment":active_comment }