from fastapi.security import OAuth2PasswordBearer
from models import User
from fastapi import Depends
from enums.user_levels import UserLevels
from database import SessionLocal


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    from auth import decode_token
    user = decode_token(token)
    return user


def get_current_user_with_level(minimum_level: UserLevels, active_state: bool = True, current_user: User = Depends(get_current_user)) -> User:
    if current_user.is_active is not active_state:
        raise Exception("User not active")

    if current_user.access_level >= minimum_level:
        return current_user
    else:
        raise Exception("Not high enough permissions")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
