
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,DateTime

from sqlalchemy_utils import EmailType,URLType
import datetime

#from courses_live.database import Base1
from talent.database import Base

class Award(Base):
    __tablename__ = "Award"

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime,default=datetime.datetime.utcnow)
    url = Column(URLType)
    title = Column(String)
    desc = Column(String)
    status = Column(Integer)