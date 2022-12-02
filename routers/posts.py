from urllib import response
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from dao.user_dao import UserDao
from schemas.user_schema import UserCreateSchema, UserSchema
from schemas.post_schema import PostCreateSchema, PostSchema
from deps import get_current_user, get_db
from models import Influencer, Post, Campaign, PostData

from datetime import datetime

router = APIRouter()

# TODO: add post (campaign, influencer) + postdata
# TODO: remove post (campaign, influencer) + postdata


@router.get("/posts/{campaign_id}", response_model=list[PostSchema])
def get_posts_by_campaign(campaign_id: int, user: str = Depends(get_current_user), db: Session = Depends(get_db)) -> list[Post]:
    campaign = db.query(Campaign).filter(
        Campaign.id == campaign_id, Campaign.user_id == user.id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    posts = db.query(Post).filter(Post.campaign_id == campaign.id).all()
    return posts


@router.get("/posts/{post_id}", response_model=PostSchema)
def get_post_by_id(post_id: int, user: str = Depends(get_current_user), db: Session = Depends(get_db)) -> Post:
    post: Post = db.query(Post).filter(Post.id == user.id).first()
    if post.campaign.user_id == user.id:
        return post
    else:
        raise HTTPException(status_code=404, detail="Post not found")



@router.post("/posts/", response_model=PostSchema)
def create_post(post_create_schema: PostCreateSchema, user: str = Depends(get_current_user), db: Session = Depends(get_db)) -> Post:
    date_added = datetime.now()
    # FOR SECURITY REASONS
    campaign = db.query(Campaign).filter(
        Campaign.id == post_create_schema.campaign_id, Campaign.user_id == user.id).first()
    influencer = db.query(Influencer).filter(
        Influencer.id == post_create_schema.influencer_id, Influencer.user_id == user.id).first()
    if not campaign or not influencer:
        raise HTTPException(status_code=404, detail="Influencer or campaign not found")


    # TODO: create redirects generation
    import random
    import string
    random_str = ''.join(random.choices(string.ascii_uppercase +
                                        string.digits, k=8))
    post = Post(url=post_create_schema.url, generated_redirect=random_str, date_added=date_added,
                influencer_id=influencer.id, campaign_id=campaign.id)
    post_data = PostData(post_id=post.id)

    db.add(post)
    db.add(post_data)
    db.commit()
    db.refresh(post)
    db.refresh(post_data)
    return post
