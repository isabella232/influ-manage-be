from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from dao.user_dao import UserDao
from schemas.user_schema import UserCreateSchema, UserSchema
from database import get_db
from models import User
from auth import get_current_user, decode_token, hash_password

router = APIRouter()


@router.post("/users/", response_model=UserSchema)
def create_user(user_schema: UserCreateSchema, db: Session = Depends(get_db)) -> User:
    user_dao = UserDao()
    db_user = user_dao.get_user_by_email(db, email=user_schema.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_dao.create_user(db=db, user_schema=user_schema)


@router.get("/users/", response_model=list[UserSchema])
def get_users(skip: int = 0, limit: int = 100, user: str = Depends(get_current_user), db: Session = Depends(get_db)) -> list[User]:
    user_dao = UserDao()
    users = user_dao.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=UserSchema)
def get_user(user: str = Depends(get_current_user), db: Session = Depends(get_db)) -> User:
    user_dao = UserDao()
    db_user = user_dao.get_user(db, user_id=user.id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")
    hashed_password = hash_password(form_data.password, user.salt)
    if not hashed_password == user.hashed_password:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")

    return {"access_token": user.email, "token_type": "bearer"}
