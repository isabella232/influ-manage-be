import database
from datetime import datetime
from sqlalchemy import desc
from models import User, Campaign, Influencer, Post, PostData
from dao.user_dao import UserDao
from schemas.campaign_schema import CampaignCreateSchema
from schemas.influencer_schema import InfluencerCreateSchema
from schemas.post_schema import PostCreateSchema
from schemas.user_schema import UserCreateSchema
db = database.SessionLocal()

usr_dao = UserDao()
u1 = usr_dao.create_user(db=db, user_schema =UserCreateSchema(email="test", password="test"))
u2 = usr_dao.create_user(db=db, user_schema =UserCreateSchema(email="tes2", password="test"))
u3 = usr_dao.create_user(db=db, user_schema =UserCreateSchema(email="test3", password="test"))
u4 = usr_dao.create_user(db=db, user_schema =UserCreateSchema(email="test4", password="test"))


campaign_schema = CampaignCreateSchema(**{
    "name": "some campaign",
    "description": "some description",
    "date_from": "2022-12-02T14:46:01.222Z",
    "date_to": "2022-12-02T14:46:01.222Z"
})

campaign1 = Campaign(name="campaign 1", user_id=u1.id,
                     description=campaign_schema.description, date_from=campaign_schema.date_from, date_to=campaign_schema.date_to, date_created=datetime.now())


campaign2 = Campaign(name="campaign 2", user_id=u1.id,
                     description=campaign_schema.description, date_from=campaign_schema.date_from, date_to=campaign_schema.date_to, date_created=datetime.now())

campaign3 = Campaign(name="campaign 3", user_id=u2.id,
                     description=campaign_schema.description, date_from=campaign_schema.date_from, date_to=campaign_schema.date_to, date_created=datetime.now())

campaign4 = Campaign(name="campaign 4", user_id=u3.id,
                     description=campaign_schema.description, date_from=campaign_schema.date_from, date_to=campaign_schema.date_to, date_created=datetime.now())

added = datetime.now()
influencer_schema = InfluencerCreateSchema(**{
    "name": "some influencer name",
    "note": "something"
})
influencer1 = Influencer(name="influencer 1",
                         note=influencer_schema.note, date_added=added, user_id=u1.id)
influencer2 = Influencer(name="influencer 2",
                         note=influencer_schema.note, date_added=added, user_id=u1.id)
influencer3 = Influencer(name="influencer 3",
                         note=influencer_schema.note, date_added=added, user_id=u2.id)
influencer4 = Influencer(name="influencer 4",
                         note=influencer_schema.note, date_added=added, user_id=u3.id)


campaign1.influencers.append(influencer1)
campaign1.influencers.append(influencer2)
campaign2.influencers.append(influencer1)
campaign3.influencers.append(influencer4)

post_create_schema = PostCreateSchema(**{
    "url": "www.something.com",
    "influencer_id": 0,
    "campaign_id": 0
})
post1 = Post(url="www.post1.com", generated_redirect="SOME 123", date_added=added,
             influencer_id=influencer1.id, campaign_id=campaign1.id)
post_data1 = PostData(post_id=post1.id)

post2 = Post(url="www.post2.com", generated_redirect="SOME 234", date_added=added,
             influencer_id=influencer2.id, campaign_id=campaign2.id)
post_data2 = PostData(post_id=post2.id)
post3 = Post(url="www.post3.com", generated_redirect="SOME 456", date_added=added,
             influencer_id=influencer1.id, campaign_id=campaign2.id)
post_data3 = PostData(post_id=post3.id)
post4 = Post(url="www.post4.com", generated_redirect="SOME 567", date_added=added,
             influencer_id=influencer3.id, campaign_id=campaign3.id)
post_data4 = PostData(post_id=post4.id)


db.add(campaign1)
db.add(campaign2)
db.add(campaign3)
db.add(campaign4)

db.add(post1)
db.add(post2)
db.add(post3)
db.add(post4)

db.add(post_data1)
db.add(post_data2)
db.add(post_data3)
db.add(post_data4)

db.add(influencer1)
db.add(influencer2)
db.add(influencer3)
db.add(influencer4)

db.commit()
