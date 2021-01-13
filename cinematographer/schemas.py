from typing import Optional
from pydantic import BaseModel
import datetime

class CinematographerBase(BaseModel):
    name :str
    desc:str
    
class CinematographerList(CinematographerBase):
    created_date: Optional[datetime.datetime]
   