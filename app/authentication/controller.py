from fastapi import APIRouter, HTTPException, Depends, Form
from fastapi.openapi.models import OAuth2
from fastapi.security.oauth2 import OAuth2AuthorizationCodeBearer, OAuth2PasswordRequestFormStrict
from sqlalchemy.orm.session import Session
from . import schemas, models
from app.utils import util, constant
import uuid, datetime
from app.talent.database import database , SessionLocal
#from configs.connection import database
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
#from users.controller import find_user_by_id
from .models import Users, Course
from app.talent.models import Talent
from app.users.controller import find_user_by_username
#from .service import verify_registration_user
router = APIRouter()
from . import py_function
from random import randint

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/auth/register", response_model = schemas.UserList)
async def register(user : schemas.UserCreate):
    userDB = await util.findExistedUser(user.username)
    if userDB:
        raise HTTPException(status_code =400, detail="Username already existed")
    #code = randint(100000,1000000)
    gid = str(uuid.uuid1())
    gdate = datetime.datetime.now()
    query = Users.__table__.insert().values(
        id = gid,
        username = user.username,
        email = user.email,
        password = util.get_password_hash(user.password),
        confirm_password =  util.get_password_hash(user.confirm_password),
        first_name = user.first_name,
        last_name = user.last_name,
        dateofbirth = user.dateofbirth,
        phone = user.phone,
        created_at = gdate,
        passcode = 0,
        is_admin = "False",
        status = "1")

    await database.execute(query)
    return {
        **user.dict(),
        "id" :gid,
        "created_at" : gdate,
        "status" : "1",
        "passcode" : 0
    }
@router.post("/auth/login", response_model = schemas.Token)
async def login(form_data : OAuth2PasswordRequestForm = Depends()):

    userDB = await util.findExistedUser(form_data.username) #(username)
    print("this is username" ,form_data.username)
    if not userDB:
        raise HTTPException(status_code = 404, detail="User Not Found")

    user = schemas.UserPWD(**userDB)
    isValid = util.verify_password(form_data.password, user.password) #(password)
    print("This is password", form_data.password)
    if not isValid:
        raise HTTPException(status_code = 404, detail="Incorrect Username Or Password")

    access_token_expires = util.timedelta(minutes=constant.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = util.create_access_token(
        data ={"sub": form_data.username},
        expires_delta= access_token_expires,
    )

    results = {
        "access_token": access_token,
        "token_type": "bearer",
        "expired_in" : constant.ACCESS_TOKEN_EXPIRE_MINUTES*60,
        "user_info" : user
    }
    return results

@router.put("/auth/update",response_model=schemas.UserList)
async def update_user(user : schemas.UserUpdate):
    gDate = datetime.datetime.now()
    query = Users.__table__.update().\
        where(Users.username == user.username).\
            values(
                first_name = user.first_name,
                last_name = user.last_name,
                email = user.email,
                phone = user.phone,
                dateofbirth = user.dateofbirth,
                created_at = gDate
            )
    await database.execute(query)
    #return {"status" : True}
    return await find_user_by_username(user.username)

@router.put("/auth/change_password", response_model=schemas.UserList)
async def change_password(user : schemas.UserChange):
    query = Users.__table__.update().\
        where(Users.username == user.username).\
            values(
                password =util.get_password_hash(user.new_password),
                confirm_password = util.get_password_hash(user.confirm_password)
            )
    await database.execute(query)
    #return {"message" : "Password Change Succesfully"}
    return await find_user_by_username(user.username)

from app.utils.util import get_current_user
@router.post("/login/test-token", response_model=schemas.UserList)
def test_token(current_user: schemas.UserInDB = Depends(get_current_user)):
    """
    Test access token.
    """
    return current_user

from app.talent.database import engine
@router.get("/search")
def get_data(search : str = "",search_type: str =" ",db: Session = Depends(get_db)):
    df = py_function.fetch_data(search,engine,search_type)
    list_of_dicts = [dict(row.items()) for row in df]
    return list_of_dicts

@router.post('/auth')
async def get_user_auth(email: str, username: str):
    #check = util.findExistedEmailUser(database=database,email=email)
    check = py_function.check_user_exist(email,engine)
    if check:
        passcode1 = await py_function.send_auth_code(email,username)
        py_function.generate_auth_email(passcode1,[email])
        return {"status":'Sent Passcode'}
    else:
        return  {"message":"Check your email-id"}

# @router.put('/auth/')
# def get_user_auth(email: str):
#     passcode = py_function.send_auth_code(email,database)
#     py_function.generate_auth_email(passcode,[email])
#     return {"status":'Sent Passcode'}

@router.post('/forget')
async def forget(email: str,username:str,passcode:int,new_pass:str,confirm_password:str):
    validate=py_function.validate_passcode(email,passcode,engine)
    if validate:
        passcode = await py_function.update_password(email,username,new_pass,confirm_password)
        py_function.generate_password_change_email([email])
        return {"status":'Success'}
    else:
        return {"status":"Passcode is wrong"}