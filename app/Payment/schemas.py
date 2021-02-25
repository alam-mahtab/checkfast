from typing import Optional
from pydantic import BaseModel
import datetime

class PaymentCreate(BaseModel):
   # id:Optional[str]
    email :str
    name:str
    amount:int

class PaymentList(BaseModel):
    id: str
    created_date : Optional[datetime.datetime]
    email :str
    name:str
    amount:int
