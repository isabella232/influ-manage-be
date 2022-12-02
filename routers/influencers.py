from cmath import inf
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from deps import get_db, get_current_user
from models import Influencer, Campaign
from schemas.influencer_schema import InfluencerSchema, InfluencerCreateSchema
from schemas.general_response_schemas import GeneralBoolResponseSchema

from datetime import datetime

router = APIRouter()


@router.get("/influencers/", response_model=list[InfluencerSchema])
def get_influencers_by_user(user: str = Depends(get_current_user), db: Session = Depends(get_db)) -> list[Influencer]:
    res = db.query(Influencer).filter(Influencer.user_id == user.id).all()
    return res


@router.get("/influencers/id/{influencer_id}", response_model=InfluencerSchema)
def get_influencer_by_id(influencer_id: int, user: str = Depends(get_current_user), db: Session = Depends(get_db)) -> Influencer:
    res = db.query(Influencer).filter(Influencer.user_id ==
                                      user.id, Influencer.id == influencer_id).first()
    if not res:
        raise HTTPException(status_code=404, detail="Influencer not found")

    return res


@router.get("/influencers/campaign/{campaign_id}", response_model=list[InfluencerSchema])
def get_influencers_by_campaign(campaign_id: int, user: str = Depends(get_current_user), db: Session = Depends(get_db)) -> list[Influencer]:
    campaign: Campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id, Campaign.user_id == user.id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    influencer_ids = [influ.id for influ in campaign.influencers]
    result = db.query(Influencer).filter(
        Influencer.id.in_(influencer_ids)).all()
    return result


@router.post("/influencers/", response_model=InfluencerSchema)
def create_influencer(influencer_schema: InfluencerCreateSchema, user: str = Depends(get_current_user), db: Session = Depends(get_db)) -> Influencer:
    added = datetime.now()
    influencer = Influencer(name=influencer_schema.name,
                            note=influencer_schema.note, date_added=added, user_id=user.id)
    db.add(influencer)
    db.commit()
    db.refresh(influencer)
    return influencer

@router.put("/influencers/{influencer_id}", response_model=InfluencerSchema)
def update_influencer(influencer_id: int, influencer_schema: InfluencerCreateSchema, user: str = Depends(get_current_user), db: Session = Depends(get_db)) -> Influencer:
    influencer: Influencer = db.query(Influencer).filter(Influencer.id == influencer_id, Influencer.user_id == user.id).first()
    influencer.name = influencer_schema.name
    influencer.note = influencer_schema.note
    db.add(influencer)
    db.commit()
    db.refresh(influencer)
    return influencer


@router.delete("/influencers/{influencer_id}", response_model=GeneralBoolResponseSchema)
def remove_influencer(influencer_id: int, user: str = Depends(get_current_user), db: Session = Depends(get_db)) -> GeneralBoolResponseSchema:
    db.query(Influencer).filter(Influencer.id == influencer_id, Influencer.user_id == user.id).delete()
    db.commit()
    db.commit()
    return GeneralBoolResponseSchema(success=True)
