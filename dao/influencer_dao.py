from models import Influencer, Campaign
from fastapi import HTTPException
from schemas.influencer_schema import InfluencerCreateSchema
from datetime import datetime
from typing import Callable, Iterator
from contextlib import AbstractContextManager
from sqlalchemy.orm import Session


class InfluencerDao:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.__session_factory = session_factory

    def get_influencers(self, user_id: int) -> list[Influencer]:
        with self.__session_factory() as db:
            res = db.query(Influencer).filter(Influencer.user_id == user_id).all()
            return res

    def get_influencers_by_campaign(
        self, user_id: int, campaign_id: int
    ) -> list[Influencer]:
        with self.__session_factory() as db:
            campaign: Campaign = (
                db.query(Campaign)
                .filter(Campaign.id == campaign_id, Campaign.user_id == user_id)
                .first()
            )
            if not campaign:
                raise HTTPException(status_code=404, detail="Campaign not found")
            influencer_ids = [influ.id for influ in campaign.influencers]
            result = (
                db.query(Influencer).filter(Influencer.id.in_(influencer_ids)).all()
            )
            return result

    def get_influencer(self, influencer_id: int, user_id: int) -> Influencer:
        with self.__session_factory() as db:
            res = (
                db.query(Influencer)
                .filter(Influencer.user_id == user_id, Influencer.id == influencer_id)
                .first()
            )
            if not res:
                raise HTTPException(status_code=404, detail="Influencer not found")

            return res

    def create_influencer(
        self, influencer_schema: InfluencerCreateSchema, user_id: int
    ) -> Influencer:
        with self.__session_factory() as db:
            added = datetime.now()
            influencer = Influencer(
                name=influencer_schema.name,
                note=influencer_schema.note,
                date_added=added,
                user_id=user_id,
            )
            db.add(influencer)
            db.commit()
            db.refresh(influencer)
            return influencer

    def update_influencer(
        self,
        influencer_id: int,
        influencer_schema: InfluencerCreateSchema,
        user_id: int,
    ) -> Influencer:
        with self.__session_factory() as db:
            influencer: Influencer = (
                db.query(Influencer)
                .filter(Influencer.id == influencer_id, Influencer.user_id == user_id)
                .first()
            )
            influencer.name = influencer_schema.name
            influencer.note = influencer_schema.note
            db.add(influencer)
            db.commit()
            db.refresh(influencer)
            return influencer

    def remove_influencer(self, influencer_id: int, user_id: int) -> bool:
        with self.__session_factory() as db:
            db.query(Influencer).filter(
                Influencer.id == influencer_id, Influencer.user_id == user_id
            ).delete()
            db.commit()
            return True
