from typing import Optional
from pydantic import BaseModel, Field
import datetime

class FreeBase(BaseModel):
    title:str
    name :str
    desc:str
    
class FreeList(FreeBase):
    created_date: Optional[datetime.datetime]

class FreeUpdate(BaseModel):
    id : str = Field(..., example="Enter Your Id")
    title:str
    name :str
    desc:str
    