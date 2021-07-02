from fastapi import FastAPI, Depends, HTTPException, applications

from schema.users import *
from crud import *
from models import users
from database.users import get_db, engine

users.Base.metadata.create_all(bind=engine)

app = FastAPI()
application = app


@app.post('/users')
def post_create_user(typed: AuthRegister, db: Session = Depends(get_db)) -> User:
    db_user = get_user_by_email(db, typed.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    typedPassword1 = typed.password1.lower()
    typedPassword2 = typed.password2.lower()
    if typedPassword1 != typedPassword2:
        raise HTTPException(status_code=400, detail="Password doesn't match")
    return create_user(db, typed)


@app.get("/users")
def get_read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user_id = Depends(auth_handler.auth_wrapper)):
    users = get_users(db, skip=skip, limit=limit)
    return users


@app.post("/auth")
def post_token_authenticate(typed: AuthLogin, db: Session = Depends(get_db)):
    user = get_user_by_email(db, email=typed.email)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid email/password")
    if (not auth_handler.verify_password(typed.password, user.hashed_password)):
        raise HTTPException(status_code=401, detail="Invalid email/password")
    token = auth_handler.encode_token(user.id)
    return {
        "token": token
    }