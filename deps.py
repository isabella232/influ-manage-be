from fastapi.security import OAuth2PasswordBearer
from models import User
from fastapi import Depends, HTTPException, status
from enums.user_levels import UserLevels
from jose import JWTError, jwt
from dao.user_dao import UserDao
from schemas.token_schema import TokenDataSchema
from commons.constants import Constants
from database import Database

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
db = Database()
user_dao = UserDao(db.session)


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, Constants.SECRET_KEY, algorithms=[Constants.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenDataSchema(username=username)
    except JWTError:
        raise credentials_exception
    user = user_dao.get_user_by_email(token_data.username)
    if user is None:
        raise credentials_exception
    return user


def get_current_user_with_level(
    minimum_level: UserLevels,
    active_state: bool = True,
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.is_active is not active_state:
        raise Exception("User not active")

    if current_user.access_level >= minimum_level:
        return current_user
    else:
        raise Exception("Not high enough permissions")
