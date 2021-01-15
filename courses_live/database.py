from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

#SQLALCHEMY_DATABASE_URL = "sqlite:///./allcourse.db"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1234@127.0.0.1/allcourse"

some_engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={}
)
SessionCourse = sessionmaker(autoflush=False ,bind=some_engine, expire_on_commit=False)
#SessionCourse = sessionmaker(autoflush=False)


Base1 = declarative_base()