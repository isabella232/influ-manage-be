import uvicorn
from fastapi import FastAPI

from database import ENGINE, Base
from routers import users, campaigns, influencers, posts, other

Base.metadata.create_all(bind=ENGINE)

app = FastAPI()
app.include_router(users.router)
app.include_router(campaigns.router)
app.include_router(influencers.router)
app.include_router(posts.router)
app.include_router(other.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
