from sqlalchemy.orm import Session

from models.user import User
from schema.user import AuthRegister
from auth import AuthHandler

auth_handler = AuthHandler()


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, typed: AuthRegister) -> User: 
    hashed_password = auth_handler.get_password_hash(typed.password1)
    db_user = User(surname=typed.surname,
                   fullname=typed.fullname,
                   email=typed.email,
                   hashed_password=hashed_password,)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
