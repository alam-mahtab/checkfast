from typing import Optional
from pydantic import BaseModel
import datetime

class EditorBase(BaseModel):
    name :str
    desc:str
    
class EditorList(EditorBase):
    created_date: Optional[datetime.datetime]
   