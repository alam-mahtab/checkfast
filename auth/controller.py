from fastapi import APIRouter, HTTPException, Depends, Form
from fastapi.openapi.models import OAuth2
from fastapi.security.oauth2 import OAuth2AuthorizationCodeBearer, OAuth2PasswordRequestFormStrict
from auth import model
from utils import util, constant
import uuid, datetime
from configs.connection import database
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
#from users.controller import find_user_by_id
from db.table import users
#from .service import verify_registration_user
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
        confirm_password =  util.get_password_hash(user.confirm_password),
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
# new routers

# @router.post("/confirm-email", response_model=model.Msg)
# async def confirm_email(uuid: model.VerificationOut):
#     if await verify_registration_user(uuid):
#         return {"msg": "Success verify email"}
#     else:
#         raise HTTPException(status_code=404, detail="Not found")

# @router.post("/password-recovery/{email}", response_model=model.Msg)
# async def recover_password(email: str, task: BackgroundTasks):
#     """ Password Recovery
#     """
#     user = await service.user_s.get_obj(email=email)
#     if not user:
#         raise HTTPException(
#             status_code=404,
#             detail="The user with this username does not exist in the system.",
#         )
#     password_reset_token = generate_password_reset_token(email)
#     task.add_task(
#         send_reset_password_email, email_to=user.email, email=email, token=password_reset_token
#     )
#     return {"msg": "Password recovery email sent"}


# @router.post("/reset-password/", response_model=Msg)
# async def reset_password(token: str = Body(...), new_password: str = Body(...)):
#     """ Reset password
#     """
#     email = verify_password_reset_token(token)
#     if not email:
#         raise HTTPException(status_code=400, detail="Invalid token")
#     user = await service.user_s.get_obj(email=email)
#     if not user:
#         raise HTTPException(
#             status_code=404,
#             detail="The user with this username does not exist in the system.",
#         )
#     elif not user.is_active:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     await service.user_s.change_password(user, new_password)
#     return {"msg": "Password updated successfully"}

#form_data : OAuth2PasswordBearer = Depends()
@router.post("/auth/login", response_model = model.Token)
#async def login(username: str,password:str):
async def login(form_data : OAuth2PasswordRequestForm = Depends()):

    userDB = await util.findExistedUser(form_data.username) #(username)
    print("this is username" ,form_data.username)
    if not userDB:
        raise HTTPException(status_code = 404, detail="User Not Found")

    user = model.UserPWD(**userDB)
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
from utils.util import get_current_user
@router.post("/login/test-token", response_model=model.UserList)
def test_token(current_user: model.UserInDB = Depends(get_current_user)):
    """
    Test access token.
    """
    return current_user
# from . import py_functions
# @router.post("/auth/login", response_model = model.Token)
# def login(email: str,password:str):
#     user_exist = py_functions.check_user_details(email,password,cnxn)
#     if user_exist>0:
#         return {"Status":"Login Successful Access Granted"}
#     else:
#         return {"Status":"Login error Access not Granted"}

# @router.post("/auth/login/", response_model = model.Token)
# async def login(username: str,password:str):
#     userDB = await util.findExistedUser(username)
#     if not userDB:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#     user = model.UserPWD(**userDB)
#     isValid = util.verify_password(password, user.password)
#     if not isValid:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")

#     return {"access_token": username, "token_type": "bearer"}
    
# # @router.put("/auth/update",response_model=model.UserList)
# # async def update_user(user : model.UserUpdate):
# #     gdate = str(datetime.datetime.now())
# #     query = users.update().\
# #         where(users.c.id == user.id).\
# #         values(
# #         username = user.username,
# #         email = user.email,
# #         #password = util.get_password_hash(user.password),#
# #         #confirm_password =  util.get_password_hash(user.confirm_password),#
# #         first_name = user.first_name,
# #         last_name = user.last_name,
# #         dateofbirth = user.dateofbirth,
# #         phone = user.phone,
# #         created_at = gdate,
# #         status = "1")
# #     await database.execute(query)

# #     #return {"status" : True}
# #     return await find_user_by_id(user.id)

@router.put("/auth/change_password",response_model=model.UserList)
async def change_password(user : model.UserChange , form_data : OAuth2PasswordRequestForm = Depends()):
    userDB = await util.findExistedUser(form_data.username)
    if not userDB:
        raise HTTPException(status_code = 404, detail="User Not Found")
    user = model.UserPWD(**userDB)
    isValid = util.verify_password(form_data.password, user.password)
    if not isValid:
        raise HTTPException(status_code = 404, detail="Incorrect Username Or Password")
    gdate = str(datetime.datetime.now())
    query = users.update().values(password = util.get_password_hash(user.password),
        confirm_password =  util.get_password_hash(user.confirm_password),
        created_at = gdate,
        status = "1")
    await database.execute(query) 
    results = {
       # "access_token": access_token,
       # "token_type": "bearer",
       # "expired_in" : constant.ACCESS_TOKEN_EXPIRE_MINUTES*60,
        "user_info" : user
    }
    return results
# @router.put("/auth/change_password",response_model=model.UserList)
# async def change_password(user : model.UserChange):
#     gdate = str(datetime.datetime.now())
#     query = users.update().\
#         where(users.c.id == user.id).\
#         values(
#         password = util.get_password_hash(user.password),
#         confirm_password =  util.get_password_hash(user.confirm_password),
#         created_at = gdate,
#         status = "1")
#     await database.execute(query)

    #return {"status" : True}
   # return await find_user_by_id(user.id)
# @router.post("/auth/forgetPassword",response_model=model.UserList)
# async def forget_password(user : model.UserReset):
#     gdate = str(datetime.datetime.now())
#     query = users.update().\
#         where(users.c.id == user.id).\
#         values(
#         password = util.get_password_hash(user.password),
#         confirm_password =  util.get_password_hash(user.confirm_password),
#         created_at = gdate,
#         status = "1")
#     await database.execute(query)

#     return {"status" : True}
    #return await find_user_by_id(user.id)
# from pathlib import Path
# @router.post("/auth/changepassword", response_model = model.Token)
# def send_reset_password_email(email_to: str, username: str):
#     subject = "{} - Password recovery for user {username}"
#     access_token_expires = util.timedelta(minutes=constant.ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = util.create_access_token(
#         data ={"sub": form_data.username},
#         expires_delta= access_token_expires,

#     with open(Path(EMAIL_TEMPLATES_DIR) / "reset_password.html") as f:
#         template_str = f.read()
#     if hasattr(token, "decode"):
#         use_token = token.decode()
#     else:
#         use_token = token
#     link = f"{SERVER_HOST}/reset-password?token={use_token}"
#     send_email(
#         email_to=email_to,
#         subject_template=subject,
#         html_template=template_str,
#         environment={
#             #"project_name": PROJECT_NAME,
#             "username": username,
#             "email": email_to,
#             "valid_hours": EMAIL_RESET_TOKEN_EXPIRE_HOURS,
#             "link": link,
#         },
#     ) 