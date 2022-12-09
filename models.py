from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    DateTime,
    Table,
    ForeignKey,
    Enum,
)
from sqlalchemy.orm import relationship
from enums.user_levels import UserLevels
from database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    salt = Column(String)
    is_active = Column(Boolean, default=True)
    access_level = Column(Enum(UserLevels), default=UserLevels.L1)
    campaigns = relationship("Campaign", back_populates="user")
    influencers = relationship("Influencer", back_populates="user")


CampaignInfluencer = Table(
    "campaign_influencer",
    Base.metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("campaign_id", ForeignKey("campaigns.id")),
    Column("influencer_id", ForeignKey("influencers.id")),
)

#TODO: MAKE unique to be unique to user only

class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    description = Column(String)
    date_from = Column(DateTime)
    date_to = Column(DateTime)
    date_created = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="campaigns", uselist=False)
    influencers = relationship(
        "Influencer", secondary=CampaignInfluencer, back_populates="campaigns", lazy='subquery'
    )
    posts = relationship("Post", back_populates="campaign", uselist=True)


class Influencer(Base):
    __tablename__ = "influencers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    note = Column(String)
    date_added = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="influencers", uselist=False)
    campaigns = relationship(
        "Campaign", secondary=CampaignInfluencer, back_populates="influencers", lazy='subquery'
    )
    posts = relationship("Post", back_populates="influencer")

#TODO: make post to have 1to1 with postdata
class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True, unique=True)
    generated_redirect = Column(String, unique=True)
    date_added = Column(DateTime)
    influencer_id = Column(Integer, ForeignKey("influencers.id"))
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    influencer = relationship("Influencer", uselist=False, back_populates="posts")
    campaign = relationship("Campaign", uselist=False, back_populates="posts")
    post_data = relationship("PostData", uselist=False, back_populates="post")


class PostData(Base):
    __tablename__ = "postdata"
    id = Column(Integer, primary_key=True, index=True)
    date_refreshed = Column(DateTime, default=datetime.now())
    num_views = Column(Integer, default=0)
    num_clicks = Column(Integer, default=0)
    num_likes = Column(Integer, default=0)
    num_comments = Column(Integer, default=0)
    num_dislikes = Column(Integer, default=0)
    post_id = Column(Integer, ForeignKey("posts.id"))
    post = relationship("Post", uselist=False, back_populates="post_data")
