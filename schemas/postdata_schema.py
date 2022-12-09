from pydantic import BaseModel

from datetime import datetime
class BasePostDataSchema(BaseModel):
    pass


class PostDataCreateSchema(BasePostDataSchema):
    pass


class PostDataSchema(BasePostDataSchema):
    id: int
    date_refreshed: datetime
    num_views: int
    num_clicks: int
    num_likes: int
    num_dislikes: int
    num_comments: int
    post_id: int

    class Config:
        orm_mode = True