from sqlalchemy import  Column, Integer, String,DateTime
from sqlalchemy_utils import URLType
import datetime
#from courses_live.database import Base1
from talent.database import Base
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
    passcode = Column(Integer)
