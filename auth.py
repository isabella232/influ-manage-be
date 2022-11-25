from fastapi.security import OAuth2PasswordBearer
from models import User
from database import get_db
from fastapi import Depends
from enums.user_levels import UserLevels
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def decode_token(token) -> User:
    # TODO: implement token decoding, this is mock
    user = next(get_db()).query(User).filter(User.id == 2).first()
    if not user:
        raise Exception("User not found")
    return user


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    user = decode_token(token)
    return user


def get_current_user_with_level(minimum_level: UserLevels, token: str = Depends(oauth2_scheme)) -> User:
    user = get_current_user(token)
    if user.access_level >= minimum_level:
        return user
    else:
        raise Exception("Not high enough permissions")


def hash_password(password: str) -> str:
    # TODO: hash password, this is mock
    return password + "HASH"
