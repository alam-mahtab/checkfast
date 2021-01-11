from typing import Optional
from pydantic import BaseModel
import datetime

class ExtensiveBase(BaseModel):
    title:str
    name :str
    desc:str
    
class ExtensiveList(ExtensiveBase):
    created_date: Optional[datetime.datetime]
   