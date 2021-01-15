from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

#SQLALCHEMY_DATABASE_URL = "sqlite:///./talent&course.db"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1234@127.0.0.1/talent&course"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={}
)
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
#SessionLocal.commit()
# with SessionLocal.no_autoflush:
#     SessionLocal.add(declarative_base)
#     SessionLocal.flush()

Base = declarative_base()