from typing import Optional
from pydantic import BaseModel
import datetime

class VideoBase(BaseModel):
    name :str
    desc:str
    
class VideoList(VideoBase):
    created_date: Optional[datetime.datetime]
   