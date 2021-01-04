from fastapi import APIRouter, HTTPException, Depends
from auth import model
from utils import util, constant
import uuid, datetime
from configs.connection import database
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from db.table import users
router = APIRouter()

@router.post("/auth/register", response_model = model.UserList)
async def register(user : model.UserCreate):
    userDB = await util.findExistedUser(user.username)
    if userDB:
        raise HTTPException(status_code =400, detail="Username already existed")
    gid = str(uuid.uuid1())
    gdate = str(datetime.datetime.now())
    query = users.insert().values(
        id = gid,
        username = user.username,
        email = user.email,
        password = util.get_password_hash(user.password),
        confirm_password = user.confirm_password,
        first_name = user.first_name,
        last_name = user.last_name,
        dateofbirth = user.dateofbirth,
        phone = user.phone,
        created_at = gdate,
        status = "1"

    )

    await database.execute(query)
    return {
        **user.dict(),
        "id" :gid,
        "created_at" : gdate,
        "status" : "1"
    }
@router.post("/auth/login", response_model = model.Token)
async def login(form_data : OAuth2PasswordRequestForm = Depends()):
    userDB = await util.findExistedUser(form_data.username)
    if not userDB:
        raise HTTPException(status_code = 404, detail="User Not Found")

    user = model.UserPWD(**userDB)
    isValid = util.verify_password(form_data.password, user.password)
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