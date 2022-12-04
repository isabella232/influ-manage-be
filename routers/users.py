from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, APIRouter, status
from sqlalchemy.orm import Session

from dao.user_dao import UserDao
from schemas.user_schema import UserCreateSchema, UserSchema
from deps import get_current_user
from models import User
from auth import AuthUtils
from schemas.token_schema import TokenSchema
from datetime import datetime, timedelta
from commons.constants import Constants
from database import SessionLocal
router = APIRouter()


@router.post("/users/", response_model=UserSchema)
def create_user(user_schema: UserCreateSchema) -> User:
    with SessionLocal() as db:
        user_dao = UserDao()
        db_user = user_dao.get_user_by_email(email=user_schema.email)
        if db_user:
            raise HTTPException(
                status_code=400, detail="Email already registered")
        return user_dao.create_user(user_schema=user_schema)


@router.post("/token", response_model=TokenSchema)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    with SessionLocal() as db:
        user_dao = UserDao()
        user = AuthUtils.authenticate_user(
            user_dao, form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(
            minutes=Constants.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = AuthUtils.create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
