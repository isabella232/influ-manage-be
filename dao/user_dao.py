from sqlalchemy.orm import Session

from models import User
from schemas.user_schema import UserCreateSchema
from auth import hash_password


class UserDao:
    def get_user(self, db: Session, user_id: int) -> User:
        return db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, db: Session, email: str) -> User:
        return db.query(User).filter(User.email == email).first()

    def get_users(self, db: Session, skip: int = 0, limit: int = 100) -> list[User]:
        return db.query(User).offset(skip).limit(limit).all()

    def create_user(self, db: Session, user_schema: UserCreateSchema) -> User:
        db_user = User(
            email=user_schema.email, hashed_password=hash_password(user_schema.password))
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
