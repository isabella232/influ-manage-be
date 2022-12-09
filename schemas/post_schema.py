from pydantic import BaseModel
from schemas.postdata_schema import PostDataSchema


class BasePostSchema(BaseModel):
    url: str


class PostCreateSchema(BasePostSchema):
    influencer_id: int
    campaign_id: int


class PostSchema(BasePostSchema):
    id: int
    post_data: PostDataSchema
    generated_redirect: str
    date_added: str
    influencer_id: int
    campaign_id: int

    class Config:
        orm_mode = True
