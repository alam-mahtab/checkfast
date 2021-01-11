from typing import Optional
from pydantic import BaseModel
import datetime
class MasterBase(BaseModel):
    title:str
    name :str
    desc:str
    
class MasterList(MasterBase):
    created_date: Optional[datetime.datetime]
   