from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from database import Base

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