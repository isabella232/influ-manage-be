from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from database import Base

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


