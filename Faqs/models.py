from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,DateTime, Table

from sqlalchemy_utils import EmailType,URLType
import datetime

#from courses_live.database import Base1
from writer.database import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime,default=datetime.datetime.utcnow)
    question = Column(String)
    answer = Column(String)
