from typing import Optional
from pydantic import BaseModel
import datetime

class WriterBase(BaseModel):
    name :str
    desc:str
    
class WriterList(WriterBase):
    created_date: Optional[datetime.datetime]
   