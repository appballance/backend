from pydantic import BaseModel


class AuthLogin(BaseModel):
    email: str
    password: str


class AuthRegister(BaseModel):
    surname: str
    fullname: str
    email: str
    password1: str
    password2: str
