from typing import Union
import datetime
from pydantic import BaseModel

class CampaignBaseSchema(BaseModel):
    name: str
    description: str
    date_from: datetime.datetime
    date_to: datetime.datetime

class CampaignCreateSchema(CampaignBaseSchema):
    user_id: int

class CampaignSchema(CampaignBaseSchema):
    id: int
    date_created: datetime.datetime
    user_id: int
    
    class Config:
        orm_mode = True
