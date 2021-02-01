from typing import Optional
from pydantic import BaseModel
import datetime
class WorkBase(BaseModel):
    name: str
    email: str
    message: str
    status:int
    
class WorkList(WorkBase):
    created_date: Optional[datetime.datetime]