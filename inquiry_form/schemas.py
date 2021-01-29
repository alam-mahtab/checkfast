from typing import Optional
from pydantic import BaseModel, Field
import datetime

class InquiryBase(BaseModel):
    title:Optional[str]
    name :str
    email :str
    desc:str
    
class FreeList(InquiryBase):
    created_date: Optional[datetime.datetime]
