from typing import Optional
from pydantic import BaseModel
import datetime

class ActorBase(BaseModel):
    name :str
    desc:str
    
class ActorList(ActorBase):
    created_date: Optional[datetime.datetime]
   