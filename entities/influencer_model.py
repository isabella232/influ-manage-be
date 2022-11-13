from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from database import Base

class Influencer(Base):
    __tablename__ = "influencers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    note = Column(String)
    date_added = Column(DateTime)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    #campaign = relationship("Campaign", back_populates="influencers")


