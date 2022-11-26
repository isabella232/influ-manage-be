from fastapi.security import OAuth2PasswordBearer
from models import User
import hashlib
from database import get_db
from fastapi import Depends
from enums.user_levels import UserLevels
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

#TODO: REFACTOR auth.py

def decode_token(token) -> User:
    # TODO: AUTHENTICATION --- implement token decoding, this is mock
    # token should be created in login phase and temporary stored so that it can be decoded here later
    # token will be stored in dictionary: {"user": [token, timestamp]}
    # if timestamp is old, generate new token, else decode, if not there - not authorized - must be generated when logging in
    user = next(get_db()).query(User).filter(User.id == 2).first()
    if not user:
        raise Exception("User not found")
    return user


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    user = decode_token(token)
    return user


def get_current_user_with_level(minimum_level: UserLevels, active_state: bool = True, current_user: User = Depends(get_current_user)) -> User:
    if current_user.is_active is not active_state:
        raise Exception("User not active")

    if current_user.access_level >= minimum_level:
        return current_user
    else:
        raise Exception("Not high enough permissions")


def hash_password(password: str, salt: str) -> str:
    return hashlib.pbkdf2_hmac(
        'sha256',  # The hash digest algorithm for HMAC
        password.encode('utf-8'),  # Convert the password to bytes
        salt,  # Provide the salt
        100000,  # It is recommended to use at least 100,000 iterations of SHA-256
        dklen=128  # Get a 128 byte key
    )
