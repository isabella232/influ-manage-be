from models import User
from schemas.user_schema import UserCreateSchema
from auth import AuthUtils
import os
from database import SessionLocal


class UserDao:
    def get_user(self, user_id: int) -> User:
        with SessionLocal() as db:
            return db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str) -> User:
        with SessionLocal() as db:
            return db.query(User).filter(User.email == email).first()

    def get_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        with SessionLocal() as db:
            return db.query(User).offset(skip).limit(limit).all()

    def create_user(self, user_schema: UserCreateSchema) -> User:
        salt = os.urandom(32)
        db_user = User(
            email=user_schema.email,
            hashed_password=AuthUtils.get_password_hash(user_schema.password),
            salt=salt,
        )
        with SessionLocal() as db:
            db.add(db_user)
            db.commit()
            db.refresh(db_user)

        return db_user
