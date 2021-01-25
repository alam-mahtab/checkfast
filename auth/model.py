from pydantic import BaseModel, Field
#from sqlalchemy.orm import models, fields
from uuid import UUID
class UserCreate(BaseModel):
    username : str 
    email : str
    password : str
    confirm_password: str
    first_name : str
    last_name : str
    dateofbirth : str
    phone : str

class UserList(BaseModel):
    id : str
    username : str
    email : str
    first_name : str
    last_name : str
    dateofbirth : str
    phone : str
    created_at : str
    status: str
class UserUpdate(BaseModel):
    id : str = Field(..., example="Enter Your Id")
    username : str 
    email : str
    #password : str
    #confirm_password: str
    first_name : str
    last_name : str
    dateofbirth : str
    phone : str
    status : str
class UserPWD(UserList):
    password : str
class UserInDB(UserList):
    salt: str = ""
    hashed_password: str = ""
class UserDelete(BaseModel):
    id : str = Field(..., example="Enter Your Id")
class UserChange(BaseModel):
   # id : str = Field(..., example="Enter Your Id")
    password : str
    confirm_password: str
class UserReset(BaseModel):
    id : str = Field(..., example="Enter Your Id")
   # username : str
    password : str
    confirm_password: str
class Token(BaseModel):
    access_token : str
    token_type : str
    #expired_in : str
    #user_info : UserList

class TokenData(BaseModel):
    username : str =None

class Msg(BaseModel):
    msg: str
class VerificationOut(BaseModel):
    link: UUID

# class Verification(models.Model):
#     """ Модель для подтверждения регистрации пользователя
#     """
#     link = fields.UUIDField(pk=True)
#     user = fields.ForeignKeyField('models.User', related_name='verification')