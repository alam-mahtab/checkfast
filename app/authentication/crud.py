from sqlalchemy.orm import Session
from app.talent.database import SessionLocal, engine, database
from app.authentication import models
from typing import Optional
import datetime

def get_email(db, username: str):
    return db.query(models.Users).filter(models.Users.username== str).first()