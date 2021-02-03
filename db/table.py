import sqlalchemy
from sqlalchemy import  Column, Integer, String,DateTime
from sqlalchemy_utils import URLType
import datetime
metadata = sqlalchemy.MetaData()
from writer.database import engine,Base
class Users(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True,unique=True)
    created_at = Column(DateTime,default=datetime.datetime.utcnow)
    username = Column(String,unique=True)
    email = Column(String)
    password = Column(String)
    confirm_password = Column(String)
    dateofbirth = Column(String)
    phone = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    status = Column(String)

    
# users = sqlalchemy.Table(
#     "users",
#     metadata,
#     sqlalchemy.Column("id", sqlalchemy.String,unique=True, primary_key=True),
#     sqlalchemy.Column("username", sqlalchemy.String, unique=True, primary_key=True),
#     sqlalchemy.Column("email", sqlalchemy.String),
#     sqlalchemy.Column("password", sqlalchemy.String),
#     sqlalchemy.Column("confirm_password", sqlalchemy.String),
#     sqlalchemy.Column("dateofbirth", sqlalchemy.String),
#     sqlalchemy.Column("first_name", sqlalchemy.String),
#     sqlalchemy.Column("last_name", sqlalchemy.String),
#     sqlalchemy.Column("phone", sqlalchemy.String),
#     sqlalchemy.Column("created_at", sqlalchemy.String),
#     sqlalchemy.Column("status", sqlalchemy.String)
# )
