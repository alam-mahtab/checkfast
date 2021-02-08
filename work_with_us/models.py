from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,DateTime
from sqlalchemy_utils import EmailType,URLType
import datetime

from sqlalchemy_utils.types import email
#from courses_live.database import Base1
from talent.database import Base

class Work(Base):
    __tablename__ = "works"

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime,default=datetime.datetime.utcnow)
    name = Column(String)
    email = Column(URLType)
    message = Column(String)
    status = Column(Integer)