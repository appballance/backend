from fastapi import FastAPI, Depends, HTTPException 
from schema.users import *
from crud import *
from database.users import get_db


app = FastAPI()


@app.post('/users')
def create_user(user: AuthRegister, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    typedPassword1 = user.password1.lower()
    typedPassword2 = user.password2.lower()
    if typedPassword1 != typedPassword2:
        raise HTTPException(status_code=400, detail="Password doesn't match")
    return create_user(db, user)


@app.get("/users/")
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users


@app.post("/auth")
def get_token_authenticate(typed: AuthLogin, db: Session = Depends(get_db)):
    user = get_user_by_email(db, email=typed.email)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid email/password")
    if (not auth_handler.verify_password(typed.password, user.email)):
        raise HTTPException(status_code=401, detail="Invalid email/password")
    token = auth_handler.encode_token(user.id)
    return {
        "token": token
    }