from typing import Optional
from pydantic import BaseModel
import datetime
class PortBase(BaseModel):
    status:int
    
class PortList(PortBase):
    created_date: Optional[datetime.datetime]