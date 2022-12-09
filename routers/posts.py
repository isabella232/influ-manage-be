from fastapi import Depends, APIRouter
from dao.post_dao import PostDao
from schemas.post_schema import PostCreateSchema, PostSchema
from deps import get_current_user
from models import Post, User
from schemas.general_response_schemas import GeneralBoolResponseSchema


router = APIRouter()
post_dao = PostDao()


@router.get("/posts/{campaign_id}", response_model=list[PostSchema])
def get_posts_by_campaign(
    campaign_id: int, user: User = Depends(get_current_user)
) -> list[Post]:
    res = post_dao.get_posts(campaign_id, user.id)
    return res


@router.get("/posts/{post_id}", response_model=PostSchema)
def get_post_by_id(post_id: int, user: User = Depends(get_current_user)) -> Post:
    res = post_dao.get_post(post_id, user.id)
    return res


@router.post("/posts/", response_model=PostSchema)
def create_post(
    post_create_schema: PostCreateSchema, user: User = Depends(get_current_user)
) -> Post:
    res = post_dao.create_post(post_create_schema, user.id)
    return res


@router.delete("/posts/{post_id}", response_model=GeneralBoolResponseSchema)
def remove_post(
    post_id: int, user: User = Depends(get_current_user)
) -> GeneralBoolResponseSchema:
    # TODO: implement remove post
    raise NotImplementedError()
