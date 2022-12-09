from models import Post, PostData, Influencer, Campaign
from fastapi import HTTPException
from schemas.post_schema import PostCreateSchema
from datetime import datetime
from typing import Callable, Iterator
from contextlib import AbstractContextManager
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

class PostDao:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.__session_factory = session_factory
    # TODO: FIX POSTS
    def get_posts(self, campaign_id: int, user_id: int) -> list[Post]:
        with self.__session_factory() as db:
            campaign = (
                db.query(Campaign)
                .filter(Campaign.id == campaign_id, Campaign.user_id == user_id)
                .first()
            )
            if not campaign:
                raise HTTPException(status_code=404, detail="Campaign not found")

            posts = db.query(Post).options(joinedload(Post.post_data)).filter(Post.campaign_id == campaign.id).all()
            return posts

    def get_post(self, post_id: int, user_id: int) -> Post:
        with self.__session_factory() as db:
            post: Post = db.query(Post).options(joinedload(Post.post_data)).filter(Post.id == user_id).first()
            if post.campaign.user_id == user_id:
                return post
            else:
                raise HTTPException(status_code=404, detail="Post not found")

    def create_post(self, post_create_schema: PostCreateSchema, user_id: int) -> Post:
        with self.__session_factory() as db:
            # TODO: simplify this
            campaign = (
                db.query(Campaign)
                .filter(
                    Campaign.id == post_create_schema.campaign_id,
                    Campaign.user_id == user_id,
                )
                .first()
            )
            influencer = (
                db.query(Influencer)
                .filter(
                    Influencer.id == post_create_schema.influencer_id,
                    Influencer.user_id == user_id,
                )
                .first()
            )
            if not campaign or not influencer:
                raise HTTPException(
                    status_code=404, detail="Influencer or campaign not found"
                )

            import random
            import string

            random_str = "".join(
                random.choices(string.ascii_uppercase + string.digits, k=8)
            )
            date_added = datetime.now()
            post = Post(
                url=post_create_schema.url,
                generated_redirect=random_str,
                date_added=date_added,
                influencer_id=influencer.id,
                campaign_id=campaign.id,
            )

            db.add(post)
            db.flush()
            post_data = PostData(post_id=post.id, post=post)
            db.add(post_data)
            db.add(post)
            db.commit()
            return post
