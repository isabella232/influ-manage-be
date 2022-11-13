from typing import Union

from pydantic import BaseModel

class CampaignBaseSchema(BaseModel):
    name: str
    description: str
    date_from: str
    date_to: str

class CampaignCreateSchema(CampaignBaseSchema):
    user_id: int

class CampaignSchema(CampaignBaseSchema):
    id: int
    date_created: str
    user_id: int
    
    class Config:
        orm_mode = True
