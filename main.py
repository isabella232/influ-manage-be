import uvicorn
from fastapi import FastAPI

from database import engine, Base
from routers import users, campaigns, influencers, posts

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(users.router)
app.include_router(campaigns.router)
app.include_router(influencers.router)
app.include_router(posts.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
