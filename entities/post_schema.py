from typing import Union

from pydantic import BaseModel
from entities.postdata_model import PostData


class Post(BaseModel):
    id: int
    url: str
    generated_redirect: str
    date_added: str
    influencer_id: int
    post_data: PostData
    class Config:
        orm_mode = True
 