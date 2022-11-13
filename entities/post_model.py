from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from database import Base

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True)
    generated_redirect = Column(String)
    date_added = Column(DateTime)
    influencer_id = Column(Integer, ForeignKey("influencers.id"))
