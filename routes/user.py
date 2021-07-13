from fastapi import FastAPI, Depends, HTTPException, applications
from sqlalchemy.orm import Session

from schema.user import *
from crud import *
from models import user
from database.people import get_db, engine

user.Base.metadata.create_all(bind=engine)

user = FastAPI()


@user.post('/users')
def post_create_user(typed: AuthRegister, db: Session = Depends(get_db)) -> User:
    db_user = get_user_by_email(db, typed.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    if typed.password1.lower() != typed.password2.lower():
        raise HTTPException(status_code=400, detail="Password doesn't match")
    return create_user(db, typed)


@user.get("/users")
def get_read_users(db: Session = Depends(get_db), user_id: int = Depends(auth_handler.auth_wrapper)):
    return get_user(db, user_id)


@user.post("/auth")
def post_token_authenticate(typed: AuthLogin, db: Session = Depends(get_db)):
    user = get_user_by_email(db, email=typed.email)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid email/password")
    if not auth_handler.verify_password(typed.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email/password")
    token = auth_handler.encode_token(user.id)
    return {
        "token": token
    }
