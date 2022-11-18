from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session

from dao.user_dao import UserDao
from schemas.user_schema import UserCreateSchema, UserSchema
from schemas.campaign_schema import CampaignSchema, CampaignCreateSchema
from models import Campaign
from datetime import datetime
from database import SessionLocal, engine, Base
Base.metadata.create_all(bind=engine)

app = FastAPI()
# TODO: create router instead of this mess

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#******************************
#******************************
#******************************
#******************************
#******************************
# ------------USER-------------
#******************************
#******************************
#******************************
#******************************

@app.post("/users/", response_model=UserSchema)
def create_user(user_schema: UserCreateSchema, db: Session = Depends(get_db)):
    user_dao = UserDao()
    db_user = user_dao.get_user_by_email(db, email=user_schema.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_dao.create_user(db=db, user_schema=user_schema)


@app.get("/users/", response_model=list[UserSchema])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    user_dao = UserDao()
    users = user_dao.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=UserSchema)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user_dao = UserDao()
    db_user = user_dao.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


#******************************
#******************************
#******************************
#******************************
#******************************
# ----------CAMPAIGN-----------
#******************************
#******************************
#******************************
#******************************

@app.post("/campaigns/{user_id}", response_model=CampaignSchema)
def create_campaign(campaign_schema: CampaignCreateSchema, db: Session = Depends(get_db)):
    date_to = datetime.now()
    date_from = datetime.now()
    date_created = datetime.now()
    campaign = Campaign(name=campaign_schema.name, user_id=campaign_schema.user_id,
                        description=campaign_schema.description, date_from=date_from, date_to=date_to, date_created=date_created)
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return campaign

@app.get("/campaigns/{user_id}", response_model=list[CampaignSchema])
def get_campaigns(user_id: int, db: Session = Depends(get_db)):
    res = db.query(Campaign).filter(Campaign.user_id == user_id).all()
    return res

@app.get("/campaigns/{campaign_id}", response_model=CampaignSchema)
def get_campaign(campaign_id: int, db: Session = Depends(get_db)):
    res = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    return res


@app.delete("/campaigns/{campaign_id}")
def remove_campaign(campaign_id: int, db: Session = Depends(get_db)):
    db.query(Campaign).filter(Campaign.id == campaign_id).delete()
    db.commit()
    return True

#TODO: Add/remove influencers from campaign
#TODO: Influencers endpoints
#TODO: Post endpoints



import uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)