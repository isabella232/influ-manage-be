from typing import Union

from pydantic import BaseModel

class Influencer(BaseModel):
    id: int
    name: str
    note: str
    date_added: str
    campaign_id: int
    class Config:
        orm_mode = True