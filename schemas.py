from typing import Union

from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

class Campaign(BaseModel):
    id: int
    name: str
    description: str
    date_from: str
    date_to: str
    date_created: str
    user_id: int
    
    class Config:
        orm_mode = True

class Influencer(BaseModel):
    id: int
    name: str
    note: str
    date_added: str
    campaign_id: int
    class Config:
        orm_mode = True

   

class PostData(BaseModel):
    id: int
    date_refreshed: str
    num_views: int
    num_clicks: int
    num_likes: int
    num_dislikes: int
    num_comments: int
    post_id: int

class Post(BaseModel):
    id: int
    url: str
    generated_redirect: str
    date_added: str
    influencer_id: int
    post_data: PostData
    class Config:
        orm_mode = True
 