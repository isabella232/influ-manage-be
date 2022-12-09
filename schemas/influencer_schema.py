from pydantic import BaseModel
from schemas.campaign_schema import CampaignSchema
import datetime


class InfluencerBaseSchema(BaseModel):
    name: str
    note: str


class InfluencerCreateSchema(InfluencerBaseSchema):
    pass


class InfluencerSchema(InfluencerBaseSchema):
    id: int
    date_added: datetime.datetime
    campaigns: list[CampaignSchema]
    user_id: int

    class Config:
        orm_mode = True
