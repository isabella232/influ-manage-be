from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from dao.user_dao import UserDao
from schemas.user_schema import UserCreateSchema, UserSchema
from deps import get_db, get_current_user
from models import User
from auth import hash_password
from schemas.token_schema import TokenSchema

router = APIRouter()


@router.post("/users/", response_model=UserSchema)
def create_user(user_schema: UserCreateSchema, db: Session = Depends(get_db)) -> User:
    user_dao = UserDao()
    db_user = user_dao.get_user_by_email(db, email=user_schema.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_dao.create_user(db=db, user_schema=user_schema)


@router.post("/token", response_model=TokenSchema)
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
