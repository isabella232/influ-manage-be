from typing import Union

from pydantic import BaseModel

class Campaign(BaseModel):
    id: int
    name: str
    description: str
    date_from: str
    date_to: str
    date_created: str
    user_id: int
    
    class Config:
        orm_mode = True
