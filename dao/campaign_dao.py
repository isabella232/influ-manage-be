from models import User
from schemas.user_schema import UserCreateSchema
from auth import AuthUtils
import os
from database import SessionLocal
from schemas.campaign_schema import CampaignSchema, CampaignCreateSchema
from models import Campaign

#TODO: implement CampaignDao
class CampaignDao:
    def create_campaign(campaign_schema: CampaignCreateSchema, user: User) -> Campaign:
        with SessionLocal() as db:
            campaign = Campaign(name=campaign_schema.name, user_id=user.id,
                                description=campaign_schema.description, date_from=campaign_schema.date_from, date_to=campaign_schema.date_to, date_created=datetime.now())
            db.add(campaign)
            db.commit()
            db.refresh(campaign)
            return campaign

