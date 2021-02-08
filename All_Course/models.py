
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,DateTime, Table

from sqlalchemy_utils import EmailType,URLType
import datetime

#from courses_live.database import Base1
from talent.database import Base

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime,default=datetime.datetime.utcnow)
    url = Column(URLType)
    title = Column(String)
    name = Column(String)
    desc = Column(String)
    type = Column(String)
    status = Column(Integer)

# from db.table import metadata
# from sqlalchemy.sql import func

# Subject = Table(
#     "Subject",
#     metadata,
#     Column("id",Integer, primary_key=True),
#     Column("created_at",DateTime,default=datetime.datetime.now(),),
#     Column("url",URLType),
#     Column("name",String),
#     Column("title",String),
#     Column("desc",String),)