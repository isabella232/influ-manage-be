from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from schemas.campaign_schema import CampaignSchema, CampaignCreateSchema
from models import Campaign, Influencer
from datetime import datetime
from deps import get_db,get_current_user


router = APIRouter()


@router.post("/campaigns/", response_model=CampaignSchema)
def create_campaign(campaign_schema: CampaignCreateSchema, user: str = Depends(get_current_user), db: Session = Depends(get_db)) -> Campaign:
    date_to = datetime.now()
    date_from = datetime.now()
    date_created = datetime.now()
    campaign = Campaign(name=campaign_schema.name, user_id=campaign_schema.user_id,
                        description=campaign_schema.description, date_from=date_from, date_to=date_to, date_created=date_created)
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return campaign


@router.get("/campaigns/", response_model=list[CampaignSchema])
def get_campaigns_by_user(user: str = Depends(get_current_user), db: Session = Depends(get_db)) -> Campaign:
    res = db.query(Campaign).filter(Campaign.user_id == user.id).all()
    return res


@router.get("/campaigns/{campaign_id}", response_model=CampaignSchema)
def get_campaign_by_id(campaign_id: int, user: str = Depends(get_current_user), db: Session = Depends(get_db)) -> Campaign:
    res = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not res:
        raise Exception("campaign not found")
    return res


@router.delete("/campaigns/{campaign_id}")
def remove_campaign(campaign_id: int, user: str = Depends(get_current_user), db: Session = Depends(get_db)) -> bool:
    db.query(Campaign).filter(Campaign.id == campaign_id).delete()
    db.commit()
    return True


@router.post("/campaigns/{campaign_id}/add-influencer")
def add_influencer_to_campaign(campaign_id: int, influencer_id: int, user: str = Depends(get_current_user), db: Session = Depends(get_db)) -> Campaign:
    campaign: Campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id).first()
    influencer: Influencer = db.query(Influencer).filter(
        Influencer.id == influencer_id).first()
    campaign.influencers.append(influencer)
    db.add(campaign)
    db.add(influencer)
    db.commit()
    db.refresh(campaign)
    db.refresh(influencer)
    return campaign


@router.delete("/campaigns/{campaign_id}/remove-influencer")
def remove_influencer_from_campaign(campaign_id: int, influencer_id: int, user: str = Depends(get_current_user), db: Session = Depends(get_db)) -> bool:
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise Exception("campaign not found")
    new_influencers = [
        influ for influ in campaign.influencers if influ.id != influencer_id]
    campaign.influencers = new_influencers
    db.add(campaign)
    db.commit()
    return True