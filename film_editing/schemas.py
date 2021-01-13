from typing import Optional
from pydantic import BaseModel
import datetime

class FilmeditBase(BaseModel):
    name :str
    desc:str
    
class FilmeditList(FilmeditBase):
    created_date: Optional[datetime.datetime]
   