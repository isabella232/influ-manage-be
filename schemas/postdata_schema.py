from pydantic import BaseModel


class BasePostDataSchema(BaseModel):
    pass


class PostDataCreateSchema(BasePostDataSchema):
    pass


class PostDataSchema(BasePostDataSchema):
    id: int
    date_refreshed: str
    num_views: int
    num_clicks: int
    num_likes: int
    num_dislikes: int
    num_comments: int
    post_id: int
