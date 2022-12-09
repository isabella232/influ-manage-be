from fastapi import Depends, APIRouter

from deps import get_current_user
from models import Influencer
from schemas.influencer_schema import InfluencerSchema, InfluencerCreateSchema
from schemas.general_response_schemas import GeneralBoolResponseSchema
from dao.influencer_dao import InfluencerDao

router = APIRouter()
influencer_dao = InfluencerDao()


@router.get("/influencers/", response_model=list[InfluencerSchema])
def get_influencers_by_user(user: str = Depends(get_current_user)) -> list[Influencer]:
    res = influencer_dao.get_influencers(user.id)
    return res


@router.get("/influencers/id/{influencer_id}", response_model=InfluencerSchema)
def get_influencer_by_id(
    influencer_id: int, user: str = Depends(get_current_user)
) -> Influencer:
    res = influencer_dao.get_influencer(influencer_id, user.id)
    return res


@router.get(
    "/influencers/campaign/{campaign_id}", response_model=list[InfluencerSchema]
)
def get_influencers_by_campaign(
    campaign_id: int, user: str = Depends(get_current_user)
) -> list[Influencer]:
    res = influencer_dao.get_influencers_by_campaign(user.id, campaign_id)
    return res


@router.post("/influencers/", response_model=InfluencerSchema)
def create_influencer(
    influencer_schema: InfluencerCreateSchema, user: str = Depends(get_current_user)
) -> Influencer:
    res = influencer_dao.create_influencer(influencer_schema, user.id)
    return res


@router.put("/influencers/{influencer_id}", response_model=InfluencerSchema)
def update_influencer(
    influencer_id: int,
    influencer_schema: InfluencerCreateSchema,
    user: str = Depends(get_current_user),
) -> Influencer:
    res = influencer_dao.update_influencer(influencer_id, influencer_schema, user.id)
    return res


@router.delete("/influencers/{influencer_id}", response_model=GeneralBoolResponseSchema)
def remove_influencer(
    influencer_id: int, user: str = Depends(get_current_user)
) -> GeneralBoolResponseSchema:
    influencer_dao.remove_influencer(influencer_id, user.id)
    return GeneralBoolResponseSchema(success=True)
