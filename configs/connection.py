import databases
import sqlalchemy
from functools import lru_cache
from configs import dbinfo
from db.table import metadata

@lru_cache
def db_config():
    return dbinfo.setting()

def DATABASE_URL(
    connection : str = db_config().db_connection,
    database : str = db_config().db_database,
    
):

    return str(connection+":///" +database)

database = databases.Database(DATABASE_URL())

engine = sqlalchemy.create_engine(
    DATABASE_URL()
)
metadata.create_all(engine)