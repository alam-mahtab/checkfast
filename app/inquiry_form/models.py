from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,DateTime, Table

from sqlalchemy_utils import EmailType,URLType
import datetime

#from courses_live.database import Base1
from app.talent.database import Base

class Inquiry(Base):
    __tablename__ = "inquiries"

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime,default=datetime.datetime.utcnow)
    name = Column(String)
    email = Column(String)
    interview = Column(Boolean, default=False)
    work_or_commision = Column(Boolean, default=False)
    other = Column(Boolean, default=False)
    title = Column(String)
    desc = Column(String)
