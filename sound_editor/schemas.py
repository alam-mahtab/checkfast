from typing import Optional
from pydantic import BaseModel
import datetime

class SoundBase(BaseModel):
    name :str
    desc:str
    
class SoundList(SoundBase):
    created_date: Optional[datetime.datetime]
   