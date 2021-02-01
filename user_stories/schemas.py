from typing import Optional
from pydantic import BaseModel
import datetime
class StoryBase(BaseModel):
    story:str
    
class StoryList(StoryBase):
    created_date: Optional[datetime.datetime]