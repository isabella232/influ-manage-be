from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from database import get_db
from models import Influencer, Campaign
from schemas.influencer_schema import InfluencerSchema, InfluencerCreateSchema
from datetime import datetime


router = APIRouter()


@router.get("/influencers/uid/{user_id}", response_model=list[InfluencerSchema])
def get_influencers_by_user(user_id: int, db: Session = Depends(get_db)):
    res = db.query(Influencer).filter(Influencer.user_id == user_id).all()
    return res


@router.get("/influencers/id/{influencer_id}", response_model=InfluencerSchema)
def get_influencer_by_id(influencer_id: int, db: Session = Depends(get_db)):
    res = db.query(Influencer).filter(Influencer.id == influencer_id).first()
    if not res:
        raise Exception("influencer not found")
    return res


@router.get("/influencers/campaign/{campaign_id}", response_model=list[InfluencerSchema])
def get_influencers_by_campaign(campaign_id: int, db: Session = Depends(get_db)):
    campaign: Campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id).first()
    if not campaign:
        raise Exception("campaign not found")
    influencer_ids = [influ.id for influ in campaign.influencers]
    result = db.query(Influencer).filter(
        Influencer.id.in_(influencer_ids)).all()
    return result


@router.post("/influencers/", response_model=InfluencerSchema)
def create_influencer(influencer_schema: InfluencerCreateSchema, db: Session = Depends(get_db)):
    added = datetime.now()
    influencer = Influencer(name=influencer_schema.name,
                            note=influencer_schema.note, date_added=added, user_id=influencer_schema.user_id)
    db.add(influencer)
    db.commit()
    db.refresh(influencer)
    return influencer


@router.delete("/influencers/{influencer_id}")
def remove_influencer(influencer_id: int, db: Session = Depends(get_db)):
    db.query(Influencer).filter(Influencer.id == influencer_id).delete()
    db.commit()
    db.commit()
    return True
