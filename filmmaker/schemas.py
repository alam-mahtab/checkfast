from typing import Optional
from pydantic import BaseModel
import datetime

class FilmmakerBase(BaseModel):
    name :str
    desc:str
    
class FilmmakerList(FilmmakerBase):
    created_date: Optional[datetime.datetime]
   