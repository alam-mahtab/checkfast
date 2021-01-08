from typing import Optional
from pydantic import BaseModel
import datetime
class TutorBase(BaseModel):
    title:str
    name :str
    desc:str
    
class TutorList(TutorBase):
    created_date: Optional[datetime.datetime]