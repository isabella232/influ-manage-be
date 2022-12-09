from fastapi import Depends, APIRouter

from schemas.campaign_schema import CampaignSchema, CampaignCreateSchema
from schemas.general_response_schemas import GeneralBoolResponseSchema
from models import Campaign, User
from deps import get_current_user
from dao.campaign_dao import CampaignDao


router = APIRouter()
campaign_dao = CampaignDao()


@router.put("/campaigns/{campaign_id}", response_model=CampaignSchema)
def update_campaign(
    campaign_id: int,
    campaign_schema: CampaignCreateSchema,
    user: User = Depends(get_current_user),
) -> Campaign:
    updated = campaign_dao.update_campaign(campaign_id, campaign_schema, user.id)
    return updated


@router.post("/campaigns/", response_model=CampaignSchema)
def create_campaign(
    campaign_schema: CampaignCreateSchema, user: User = Depends(get_current_user)
) -> Campaign:
    campaign = campaign_dao.create_campaign(campaign_schema, user.id)
    return campaign


@router.get("/campaigns/", response_model=list[CampaignSchema])
def get_campaigns_by_user(user: str = Depends(get_current_user)) -> Campaign:
    campaigns = campaign_dao.get_campaigns(user.id)
    return campaigns


@router.get("/campaigns/{campaign_id}", response_model=CampaignSchema)
def get_campaign_by_id(
    campaign_id: int, user: User = Depends(get_current_user)
) -> Campaign:
    campaign = campaign_dao.get_campaign(campaign_id, user.id)
    return campaign


@router.delete("/campaigns/{campaign_id}", response_model=GeneralBoolResponseSchema)
def remove_campaign(
    campaign_id: int, user: User = Depends(get_current_user)
) -> GeneralBoolResponseSchema:
    campaign_dao.remove_campaign(campaign_id, user.id)
    return GeneralBoolResponseSchema(success=True)


@router.post(
    "/campaigns/{campaign_id}/add-influencer", response_model=GeneralBoolResponseSchema
)
def add_influencer_to_campaign(
    campaign_id: int, influencer_id: int, user: User = Depends(get_current_user)
) -> GeneralBoolResponseSchema:
    campaign_dao.add_influencer(campaign_id, influencer_id, user.id)
    return GeneralBoolResponseSchema(success=True)


@router.delete(
    "/campaigns/{campaign_id}/remove-influencer",
    response_model=GeneralBoolResponseSchema,
)
def remove_influencer_from_campaign(
    campaign_id: int, influencer_id: int, user: User = Depends(get_current_user)
) -> GeneralBoolResponseSchema:
    campaign_dao.remove_influencer(campaign_id, influencer_id, user.id)
    return GeneralBoolResponseSchema(success=True)
