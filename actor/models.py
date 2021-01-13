from sqlalchemy import  Column, Integer, String,DateTime
from sqlalchemy_utils import URLType
import datetime
from writer.database import Base

class Actor(Base):
    __tablename__ = "actors"

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime,default=datetime.datetime.utcnow)
    url_profile = Column(URLType)
    url_cover = Column(URLType)
    name = Column(String)
    desc = Column(String)
    


   