from sqlalchemy import  Column, Integer, String,DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import URLType
import datetime
from app.talent.database import Base

class Talent(Base):
    __tablename__ = "talents"

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime,default=datetime.datetime.utcnow)
    url_profile = Column(URLType)
    url_cover = Column(URLType)
    name = Column(String)
    desc = Column(String)
    type = Column(String)
    status = Column(Integer)
    connect = relationship('Honour', back_populates='conn')
    port_connect = relationship('Port', back_populates='port_conn')

class Honour(Base):
    __tablename__ = "honours"

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime,default=datetime.datetime.utcnow)
    url = Column(URLType)
    name = Column(String)
    desc = Column(String)
    status = Column(Integer)
    talent_id = Column(Integer, ForeignKey('talents.id'))
    conn = relationship('Talent', back_populates='connect')

class Port(Base):
    __tablename__ = "ports"

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime,default=datetime.datetime.utcnow)
    url = Column(URLType)
    status = Column(Integer)
    talent_id = Column(Integer, ForeignKey('talents.id'))
    port_conn = relationship('Talent', back_populates='port_connect')


   