import databases
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from app.configs import dbinfo
#from db.table import metadata
import cloudinary

cloudinary.config(
    cloud_name = "alamcloud",
    api_key = "376629981897418",
    api_secret = "eSWZxKVVqisGZ_FIzCigU-JE_6I"
)



def db_config():
    return dbinfo.setting()

def DATABASE_URL(

    database : str = db_config().db_stringpost
    #database : str = db_config().db_stringlite
    
):

    #return str(connection+":///" +database)
    return str(database)

#SQLALCHEMY_DATABASE_URL = "sqlite:///./test11.db"
# For local connection
#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Pass2020!@65.1.64.150:5432/Cinedarbaar" 

#SQLALCHEMY_DATABASE_URL ="psql --host=cd.csorhad7ihl5.ap-south-1.rds.amazonaws.com --port=5432 --username=postgres --password=Mobirizer12345 --dbname=cd"
# For aws connection
#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Mobirizer12345@cd.csorhad7ihl5.ap-south-1.rds.amazonaws.com:5432/cd" 
#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Mobirizer12345@172.31.15.218:5432/cd" 

#SQLALCHEMY_DATABASE_URL = "postgres://postgres:Mobirizer2021@database-1.csorhad7ihl5.ap-south-1.rds.amazonaws.com" 
#db_string = "postgres://admin:donotusethispassword@aws-us-east-1-portal.19.dblayer.com:15813/compose"
# For Heroku connection
#SQLALCHEMY_DATABASE_URL = "postgres://qfawfnaslzovwe:03ef650b17a8e85da0081d5522e11f0a85d667369feb88da97c1b3e968482f81@ec2-54-86-189-179.compute-1.amazonaws.com:5432/d5cu3ni8p963j9"


#database =databases.Database(SQLALCHEMY_DATABASE_URL)
database =databases.Database(DATABASE_URL())


# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={}
# )

engine = create_engine(
    DATABASE_URL(), connect_args={}
)
SessionLocal = sessionmaker(autoflush=False ,bind=engine, expire_on_commit=False)
# metadata.create_all(engine)
# session = sessionmaker()()
#SessionLocal.commit()
# with SessionLocal.no_autoflush:
#     SessionLocal.add(declarative_base)
#     SessionLocal.flush()

Base = declarative_base()

