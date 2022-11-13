from sqlalchemy.orm import Session

from entities.user_model import User
from entities.user_schema import UserCreateSchema
class UserDao:
    def get_user(self, db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()


    def get_user_by_email(self, db: Session, email: str):
        return db.query(User).filter(User.email == email).first()


    def get_users(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(User).offset(skip).limit(limit).all()


    def create_user(self, db: Session, user_schema: UserCreateSchema):
        fake_hashed_password = user_schema.password + "notreallyhashed"
        db_user = User(
            email=user_schema.email, hashed_password=fake_hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user