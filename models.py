from sqlalchemy import Boolean, Column, Integer, String, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    campaigns = relationship("Campaign", back_populates="user")
    influencers = relationship("Influencer", back_populates="user")


CampaignInfluencer = Table(
    "campaign_influencer",
    Base.metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("campaign_id", ForeignKey("campaigns.id")),
    Column("influencer_id", ForeignKey("influencers.id")),
)


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
        "Influencer", secondary=CampaignInfluencer, back_populates="campaigns"
    )


class Influencer(Base):
    __tablename__ = "influencers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    note = Column(String)
    date_added = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="influencers", uselist=False)
    campaigns = relationship(
        "Campaign", secondary=CampaignInfluencer, back_populates="influencers"
    )
    posts = relationship("Post", back_populates="influencer")


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True, unique=True)
    generated_redirect = Column(String,  unique=True)
    date_added = Column(DateTime)
    influencer_id = Column(Integer, ForeignKey("influencers.id"))
    influencer = relationship(
        "Influencer", uselist=False, back_populates="posts")
    post_data = relationship("PostData", uselist=False, back_populates="post")


class PostData(Base):
    __tablename__ = "postdata"
    id = Column(Integer, primary_key=True, index=True)
    date_refreshed = Column(DateTime)
    num_views = Column(Integer)
    num_clicks = Column(Integer)
    num_likes = Column(Integer)
    num_comments = Column(Integer)
    num_dislikes = Column(Integer)
    post_id = Column(Integer, ForeignKey("posts.id"))
    post = relationship("Post", uselist=False, back_populates="post_data")
