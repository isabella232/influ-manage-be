from typing import Union

from pydantic import BaseModel
from schemas.campaign_schema import CampaignSchema
import datetime


class InfluencerBaseSchema(BaseModel):
    user_id: int
    name: str
    note: str


class InfluencerCreateSchema(InfluencerBaseSchema):
    pass


class InfluencerSchema(InfluencerBaseSchema):
    id: int
    date_added: datetime.datetime
    campaigns: list[CampaignSchema]

    class Config:
        orm_mode = True
