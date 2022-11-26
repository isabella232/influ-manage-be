from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from dao.user_dao import UserDao
from schemas.user_schema import UserCreateSchema, UserSchema
from deps import get_db


router = APIRouter()

# TODO: add post (campaign, influencer) + postdata
# TODO: remove post (campaign, influencer) + postdata