from passlib.context import CryptContext
from datetime import datetime, timedelta
from commons.constants import Constants
from jose import JWTError, jwt


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# TODO: REFACTOR auth.py


class AuthUtils:
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)

    @staticmethod
    def authenticate_user(user_dao, username: str, password: str):
        user = user_dao.get_user_by_email(username)
        if not user:
            return False
        if not AuthUtils.verify_password(password, user.hashed_password):
            return False
        return user

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, Constants.SECRET_KEY, algorithm=Constants.ALGORITHM)
        return encoded_jwt