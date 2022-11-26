from fastapi.security import OAuth2PasswordBearer
from models import User
import hashlib
from deps import get_db
from fastapi import Depends
from enums.user_levels import UserLevels

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

def hash_password(password: str, salt: str) -> str:
    return hashlib.pbkdf2_hmac(
        'sha256',  # The hash digest algorithm for HMAC
        password.encode('utf-8'),  # Convert the password to bytes
        salt,  # Provide the salt
        100000,  # It is recommended to use at least 100,000 iterations of SHA-256
        dklen=128  # Get a 128 byte key
    )
