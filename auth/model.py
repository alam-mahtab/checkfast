from pydantic import BaseModel, Field

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

class UserPWD(UserList):
    password : str

class Token(BaseModel):
    access_token : str
    token_type : str
    expired_in : str
    user_info : UserList