from typing import Optional
from pydantic import BaseModel
import datetime

class TalentBase(BaseModel):
    name :str
    desc:str
    type:str
    status:int
    
class TalentList(TalentBase):
    created_date: Optional[datetime.datetime]
   