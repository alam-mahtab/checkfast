from typing import Optional
from pydantic import BaseModel
import datetime
class MicroBase(BaseModel):
    title:str
    name :str
    desc:str
    
class MicroList(MicroBase):
    created_date: Optional[datetime.datetime]
   