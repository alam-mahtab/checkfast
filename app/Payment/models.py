from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,DateTime

from sqlalchemy_utils import EmailType,URLType
import datetime
from app.talent.database import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(String, primary_key=True,unique=True)
    created_date = Column(DateTime,default=datetime.datetime.utcnow)
    email = Column(String)
    name = Column(String)
    amount = Column(Integer)