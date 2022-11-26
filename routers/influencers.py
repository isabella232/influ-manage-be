from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from deps import get_db, get_current_user
from models import Influencer, Campaign
from schemas.influencer_schema import InfluencerSchema, InfluencerCreateSchema
from datetime import datetime

router = APIRouter()


@router.get("/influencers/uid/{user_id}", response_model=list[InfluencerSchema])
def get_influencers_by_user(user: str = Depends(get_current_user), db: Session = Depends(get_db)) -> list[Influencer]:
    res = db.query(Influencer).filter(Influencer.user_id == user.id).all()
    return res


@router.get("/influencers/id/{influencer_id}", response_model=InfluencerSchema)
def get_influencer_by_id(influencer_id: int, user: str = Depends(get_current_user), db: Session = Depends(get_db)) -> Influencer:
    res = db.query(Influencer).filter(Influencer.id == influencer_id).first()
    if not res:
        raise Exception("influencer not found")
    return res


@router.get("/influencers/campaign/{campaign_id}", response_model=list[InfluencerSchema])
def get_influencers_by_campaign(campaign_id: int, user: str = Depends(get_current_user), db: Session = Depends(get_db)) -> list[Influencer]:
    campaign: Campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id).first()
    if not campaign:
        raise Exception("campaign not found")
    influencer_ids = [influ.id for influ in campaign.influencers]
    result = db.query(Influencer).filter(
        Influencer.id.in_(influencer_ids)).all()
    return result


@router.post("/influencers/", response_model=InfluencerSchema)
def create_influencer(influencer_schema: InfluencerCreateSchema, user: str = Depends(get_current_user), db: Session = Depends(get_db)) -> Influencer:
    added = datetime.now()
    influencer = Influencer(name=influencer_schema.name,
                            note=influencer_schema.note, date_added=added, user_id=influencer_schema.user_id)
    db.add(influencer)
    db.commit()
    db.refresh(influencer)
    return influencer


@router.delete("/influencers/{influencer_id}")
def remove_influencer(influencer_id: int, user: str = Depends(get_current_user), db: Session = Depends(get_db)) -> bool:
    db.query(Influencer).filter(Influencer.id == influencer_id).delete()
    db.commit()
    db.commit()
    return True
