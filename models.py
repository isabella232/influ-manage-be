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


campaign_influencer = Table(
    "campaign_influencer",
    Base.metadata,
    Column("campaign_id", ForeignKey("campaigns.id"), primary_key=True),
    Column("influencer_id", ForeignKey("influencers.id"), primary_key=True),
)

class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    date_from = Column(DateTime)
    date_to = Column(DateTime)
    date_created = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="campaigns")
    influencers = relationship(
        "Influencer", secondary="campaign_influencer", back_populates="campaigns"
    )

class Influencer(Base):
    __tablename__ = "influencers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    note = Column(String)
    date_added = Column(DateTime)
    campaigns = relationship(
        "Influencer", secondary="campaign_influencer", back_populates="influencers"
    )
    posts = relationship("Post", back_populates="influencer")
    
class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True)
    generated_redirect = Column(String)
    date_added = Column(DateTime)
    influencer_id = Column(Integer, ForeignKey("influencers.id"))
    influencer = relationship("Influencer", back_populates="posts")
    post_data = relationship("PostData", back_populates="post")

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
    post = relationship("Post", back_populates="post_data")

