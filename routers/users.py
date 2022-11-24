from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from dao.user_dao import UserDao
from schemas.user_schema import UserCreateSchema, UserSchema
from database import get_db


router = APIRouter()

@router.post("/users/", response_model=UserSchema)
def create_user(user_schema: UserCreateSchema, db: Session = Depends(get_db)):
    user_dao = UserDao()
    db_user = user_dao.get_user_by_email(db, email=user_schema.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_dao.create_user(db=db, user_schema=user_schema)


@router.get("/users/", response_model=list[UserSchema])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    user_dao = UserDao()
    users = user_dao.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=UserSchema)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user_dao = UserDao()
    db_user = user_dao.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user