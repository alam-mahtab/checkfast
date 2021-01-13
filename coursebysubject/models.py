
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,DateTime

from sqlalchemy_utils import EmailType,URLType
import datetime

from courses_live.database import Base

class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime,default=datetime.datetime.utcnow)
    url = Column(URLType)
    title = Column(String)
    name = Column(String)
    desc = Column(String)