from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

SQLALCHEMY_DATABASE_URL = "sqlite:///./allcourse.db"
#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1234@127.0.0.1/allcourse"

# Heroku Connection
#SQLALCHEMY_DATABASE_URL = "postgres://pabzjsrsctrfvp:4ffd0617efde5cdae2d60b2b24b9f378ae832a2bb56c2eca8b83f10697c022f7@ec2-107-23-191-123.compute-1.amazonaws.com:5432/dcunjfn20d8pi0" 


some_engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={}
)
SessionCourse = sessionmaker(autoflush=False ,bind=some_engine, expire_on_commit=False)
#SessionCourse = sessionmaker(autoflush=False)


Base1 = declarative_base()