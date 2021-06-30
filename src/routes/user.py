from fastapi import FastAPI, Depends, HTTPException
from auth import AuthHandler
from schema.user import AuthLogin, AuthRegister
from database.users import users
 


app = FastAPI()
auth_handler = AuthHandler()


@app.post('/register', status_code=201)
def register(typed: AuthRegister):

    typedEmail = typed.email.lower()
    
    if any(x['email'] == typedEmail for x in users):
        return ({
            "status": 400,
            "message": "Email already exists"
        })
    
    typedPassword1 = typed.password1.lower()
    typedPassword2 = typed.password2.lower()
    
    if typedPassword1 != typedPassword2:
        return ({
            "status": 400,
            "message": "Password doesn't match"
        })      
    users.append({
        "surname": typed.surname.lower(),
        "fullname": typed.fullname.lower(),
        "email": typedEmail,
        "password": auth_handler.get_password_hash(typed.password1),  
    })
    return users


@app.post('/login')
def login(typed: AuthLogin):
    user = None
    id = -1
    for i, x in enumerate(users):
        if x['email'] == typed.email:
            user = x
            id = i
            break
    
    if (user is None) or (not auth_handler.verify_password(typed.password, user['password'])):
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_token(id)
    return { 'token': token }


@app.get('/home')
def protected(user_id=Depends(auth_handler.auth_wrapper)):
    return { 'user': users[user_id] }