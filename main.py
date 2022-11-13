from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from dao.user_dao import UserDao
from entities.user_schema import UserCreate, User

from database import SessionLocal, engine, Base
Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_dao = UserDao()
    db_user = user_dao.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_dao.create_user(db=db, user=user)


@app.get("/users/", response_model=list[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    user_dao = UserDao()
    users = user_dao.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user_dao = UserDao()
    db_user = user_dao.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
