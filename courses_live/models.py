from sqlalchemy import  Column, Integer, String,DateTime
from sqlalchemy_utils import URLType
import datetime
#from courses_live.database import Base1
from writer.database import Base

class Live(Base):
    __tablename__ = "lives"

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime,default=datetime.datetime.utcnow)
    url = Column(URLType)
    title = Column(String)
    name = Column(String)
    desc = Column(String)
    


   