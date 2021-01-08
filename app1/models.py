
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,DateTime

from sqlalchemy_utils import EmailType,URLType
import datetime

from app1.database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime,default=datetime.datetime.utcnow)
    url = Column(URLType)
    title = Column(String)
    name = Column(String)
    desc = Column(String)
    

   