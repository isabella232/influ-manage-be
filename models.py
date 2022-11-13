from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    #campaings = relationship("Campaign", back_populates="owner")


class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    date_from = Column(DateTime)
    date_to = Column(DateTime)
    date_created = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id"))

    #user = relationship("User", back_populates="campaigns")

class Influencer(Base):
    __tablename__ = "influencers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    note = Column(String)
    date_added = Column(DateTime)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    #campaign = relationship("Campaign", back_populates="influencers")

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True)
    generated_redirect = Column(String)
    date_added = Column(DateTime)
    influencer_id = Column(Integer, ForeignKey("influencers.id"))

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


