import databases
import sqlalchemy
from sqlalchemy import (Column, DateTime, Integer, MetaData, String, Table,create_engine)
from sqlalchemy.sql import func
from sqlalchemy_utils import URLType
from configs import dbinfo
from db.table import metadata



def db_config():
    return dbinfo.setting()

def DATABASE_URL(
    connection : str = db_config().db_connection,
    database : str = db_config().db_database,
    
):

    return str(connection+":///" +database)
# extensive course
extensive_course = Table(
    "extensive_course",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("Name", String(50)),
    Column("title", String(50)),
    Column("description", String(50)),
    Column("created_date", DateTime, default=func.now(), nullable=False),
)
# comnotes of Comments
comnotes = Table(
    "comnotes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("Name", String(50)),
    Column("title", String(50)),
    Column("description", String(50)),
    Column("created_date", DateTime, default=func.now(), nullable=False),
)
# fnotes of feed
fnotes = Table(
    "fnotes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("url", URLType ),
    Column("Name", String(50)),
    Column("title", String(50)),
    Column("description", String(50)),
    Column("created_date", DateTime, default=func.now(), nullable=False),
)
#liveapp

posts = Table(
    "posts",
    metadata,
    Column("id",Integer, primary_key=True),
    Column("created_at",DateTime,default=func.now(),),
    Column("url",URLType),
    Column("name",String),
    Column("title",String),
    Column("desc",String),)

database = databases.Database(DATABASE_URL())

engine = sqlalchemy.create_engine(
    DATABASE_URL()
)



metadata.create_all(engine)
