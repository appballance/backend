from pydantic import BaseModel
# from pylance import Optional


class AuthLogin(BaseModel):
    email: str
    password: str

class AuthRegister(BaseModel):
    surname: str
    fullname: str
    email: str
    password1: str
    password2: str


# class IdentityBase(BaseModel):
#     balance: Optional[int] = 0


# class IdentityCreate(IdentityBase):
#     pass