from models import Influencer
from database import SessionLocal
from schemas.campaign_schema import CampaignCreateSchema
from models import Campaign
from fastapi import HTTPException
from datetime import datetime


class CampaignDao:
    def create_campaign(
        self, campaign_schema: CampaignCreateSchema, user_id: int
    ) -> Campaign:
        with SessionLocal() as db:
            campaign = Campaign(
                name=campaign_schema.name,
                user_id=user_id,
                description=campaign_schema.description,
                date_from=campaign_schema.date_from,
                date_to=campaign_schema.date_to,
                date_created=datetime.now(),
            )
            db.add(campaign)
            db.commit()
            db.refresh(campaign)
            return campaign

    def update_campaign(
        self, campaign_id: int, updated_schema: CampaignCreateSchema, user_id: int
    ) -> Campaign:
        with SessionLocal() as db:
            campaign: Campaign = (
                db.query(Campaign)
                .filter(Campaign.id == campaign_id, Campaign.user_id == user_id)
                .first()
            )
            campaign.date_from = updated_schema.date_from
            campaign.date_to = updated_schema.date_to
            campaign.description = updated_schema.description
            campaign.name = updated_schema.name
            db.add(campaign)
            db.commit()
            db.refresh(campaign)
            return campaign

    def get_campaign(self, campaign_id: int, user_id: int) -> Campaign:
        with SessionLocal() as db:
            campaign = (
                db.query(Campaign)
                .filter(Campaign.id == campaign_id, Campaign.user_id == user_id)
                .first()
            )
            if not campaign:
                raise HTTPException(status_code=404, detail="Campaign not found")
            return campaign

    def get_campaigns(self, user_id: int) -> list[Campaign]:
        with SessionLocal() as db:
            res = db.query(Campaign).filter(Campaign.user_id == user_id).all()
            return res

    def remove_campaign(self, campaign_id: int, user_id: int) -> bool:
        with SessionLocal() as db:
            db.query(Campaign).filter(
                Campaign.id == campaign_id, Campaign.user_id == user_id
            ).delete()
            db.commit()
            return True

    def add_influencer(
        self, campaign_id: int, influencer_id: int, user_id: int
    ) -> bool:
        with SessionLocal() as db:
            campaign: Campaign = (
                db.query(Campaign)
                .filter(Campaign.id == campaign_id, Campaign.user_id == user_id)
                .first()
            )
            influencer: Influencer = (
                db.query(Influencer)
                .filter(Influencer.id == influencer_id, Influencer.user_id == user_id)
                .first()
            )
            if not campaign or not influencer:
                raise HTTPException(
                    status_code=404, detail="Campaign or Influencer not found"
                )
            campaign.influencers.append(influencer)
            db.add(campaign)
            db.add(influencer)
            db.commit()
            db.refresh(campaign)
            db.refresh(influencer)
            return True

    def remove_influencer(
        self, campaign_id: int, influencer_id: int, user_id: int
    ) -> bool:
        with SessionLocal() as db:
            campaign = (
                db.query(Campaign)
                .filter(Campaign.id == campaign_id, Campaign.user_id == user_id)
                .first()
            )
            if not campaign:
                raise HTTPException(status_code=404, detail="Campaign not found")
            new_influencers = [
                influ for influ in campaign.influencers if influ.id != influencer_id
            ]
            campaign.influencers = new_influencers
            db.add(campaign)
            db.commit()
            return True
