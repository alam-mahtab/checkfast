from typing import Optional
from pydantic import BaseModel, Field
import datetime

class InquiryBase(BaseModel):
    question :str
    answer :str
    
class FreeList(InquiryBase):
    created_date: Optional[datetime.datetime]