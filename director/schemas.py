from typing import Optional
from pydantic import BaseModel
import datetime

class DirectorBase(BaseModel):
    name :str
    desc:str
    
class DirectorList(DirectorBase):
    created_date: Optional[datetime.datetime]
   