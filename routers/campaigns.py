from fastapi import Depends, APIRouter, HTTPException

from schemas.campaign_schema import CampaignSchema, CampaignCreateSchema
from schemas.general_response_schemas import GeneralBoolResponseSchema
from models import Campaign, Influencer, User
from datetime import date, datetime
from deps import get_current_user
from database import SessionLocal
from dao.campaign_dao import CampaignDao


router = APIRouter()
campaign_dao = CampaignDao()

@router.put("/campaigns/{campaign_id}", response_model=CampaignSchema)
def update_campaign(campaign_id: int, campaign_schema: CampaignCreateSchema, user: User = Depends(get_current_user)) -> Campaign:
    with SessionLocal() as db:
        campaign: Campaign = db.query(Campaign).filter(
            Campaign.id == campaign_id, Campaign.user_id == user.id).first()
        campaign.date_from = campaign_schema.date_from
        campaign.date_to = campaign_schema.date_to
        campaign.description = campaign_schema.description
        campaign.name = campaign_schema.name
        db.add(campaign)
        db.commit()
        db.refresh(campaign)
        return campaign


@router.post("/campaigns/", response_model=CampaignSchema)
def create_campaign(campaign_schema: CampaignCreateSchema, user: User = Depends(get_current_user)) -> Campaign:
    campaign = campaign_dao.create_campaign(campaign_schema, user)
    return campaign


@router.get("/campaigns/", response_model=list[CampaignSchema])
def get_campaigns_by_user(user: str = Depends(get_current_user)) -> Campaign:
    with SessionLocal() as db:
        res = db.query(Campaign).filter(Campaign.user_id == user.id).all()
        return res


@router.get("/campaigns/{campaign_id}", response_model=CampaignSchema)
def get_campaign_by_id(campaign_id: int, user: User = Depends(get_current_user)) -> Campaign:
    with SessionLocal() as db:
        res = db.query(Campaign).filter(
            Campaign.id == campaign_id, Campaign.user_id == user.id).first()
        if not res:
            raise HTTPException(status_code=404, detail="Campaign not found")
        return res


@router.delete("/campaigns/{campaign_id}", response_model=GeneralBoolResponseSchema)
def remove_campaign(campaign_id: int, user: User = Depends(get_current_user)) -> bool:
    with SessionLocal() as db:
        db.query(Campaign).filter(Campaign.id == campaign_id,
                                  Campaign.user_id == user.id).delete()
        db.commit()
        return GeneralBoolResponseSchema(success=True)


@router.post("/campaigns/{campaign_id}/add-influencer", response_model=GeneralBoolResponseSchema)
def add_influencer_to_campaign(campaign_id: int, influencer_id: int, user: User = Depends(get_current_user)) -> Campaign:
    with SessionLocal() as db:
        campaign: Campaign = db.query(Campaign).filter(
            Campaign.id == campaign_id, Campaign.user_id == user.id).first()
        influencer: Influencer = db.query(Influencer).filter(
            Influencer.id == influencer_id, Influencer.user_id == user.id).first()
        if not campaign or not influencer:
            raise HTTPException(
                status_code=404, detail="Campaign or Influencer not found")
        campaign.influencers.append(influencer)
        db.add(campaign)
        db.add(influencer)
        db.commit()
        db.refresh(campaign)
        db.refresh(influencer)
        return GeneralBoolResponseSchema(success=True)


@router.delete("/campaigns/{campaign_id}/remove-influencer", response_model=GeneralBoolResponseSchema)
def remove_influencer_from_campaign(campaign_id: int, influencer_id: int, user: User = Depends(get_current_user)) -> bool:
    with SessionLocal() as db:
        campaign = db.query(Campaign).filter(
            Campaign.id == campaign_id, Campaign.user_id == user.id).first()
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")
        new_influencers = [
            influ for influ in campaign.influencers if influ.id != influencer_id]
        campaign.influencers = new_influencers
        db.add(campaign)
        db.commit()
        return GeneralBoolResponseSchema(success=True)
