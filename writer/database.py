from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

SQLALCHEMY_DATABASE_URL = "sqlite:///./talent&course.db"
# For local connection
#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1234@127.0.0.1/talent&course" 

#SQLALCHEMY_DATABASE_URL ="psql --host=cd.csorhad7ihl5.ap-south-1.rds.amazonaws.com --port=5432 --username=postgres --password=Mobirizer12345 --dbname=cd"
# For aws connection
#SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:Mobirizer12345@cd.csorhad7ihl5.ap-south-1.rds.amazonaws.com:5432/cd" 
#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Mobirizer12345@172.31.15.218/cd" 

SQLALCHEMY_DATABASE_URL = "postgres://postgres:Mobirizer2021@database-1.csorhad7ihl5.ap-south-1.rds.amazonaws.com:5432/database-1" 

# For Heroku connection
#SQLALCHEMY_DATABASE_URL = "postgres://pabzjsrsctrfvp:4ffd0617efde5cdae2d60b2b24b9f378ae832a2bb56c2eca8b83f10697c022f7@ec2-107-23-191-123.compute-1.amazonaws.com:5432/dcunjfn20d8pi0"
 


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={}
)
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
#SessionLocal.commit()
# with SessionLocal.no_autoflush:
#     SessionLocal.add(declarative_base)
#     SessionLocal.flush()

Base = declarative_base()