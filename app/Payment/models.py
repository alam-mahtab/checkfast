from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,DateTime
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType,URLType
import datetime
from app.talent.database import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True,unique=True)
    created_date = Column(DateTime,default=datetime.datetime.utcnow)
    pay_id = Column(String)
    amount = Column(String)
    currency = Column(String)
    receipt = Column(String)
    status = Column(String)
    pay_createdat = Column(String)
    clients_id = Column(String, ForeignKey('users.id'))
    clients = relationship('Users', back_populates='paid3')
    courses_id = Column(Integer, ForeignKey('courses.id'))
    courses = relationship('Course', back_populates='paid2')