from balance.schemas.user_schemas import AuthLogin
from balance.models.user_models import User

from balancelib.auth import AuthHandler

from sqlalchemy.orm import Session

from fastapi import HTTPException


class PostTokenAuthenticateResponseModel:
    def __init__(self, token):
        self.token = token

    def __call__(self):
        return self.token


class PostTokenAuthenticateRequestModel:
    def __init__(self, user: AuthLogin):
        self.email = user.email
        self.password = user.password


class PostTokenAuthenticateInteractor:
    def __init__(self,
                 request: PostTokenAuthenticateRequestModel,
                 adapter: Session):
        self.request = request
        self.adapter = adapter

    def _get_user_by_email(self):
        return self.adapter.query(User).filter(
            User.email == self.request.email).first()

    @staticmethod
    def _check_user_not_exists(user: User):
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid email/password")

    def _verify_password(self, user: User):
        if not AuthHandler().verify_password(self.request.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid email/password")

    @staticmethod
    def _generate_token(user: User):
        token = AuthHandler().encode_token(user.id)
        return {"token": token}

    def run(self):
        user = self._get_user_by_email()
        self._check_user_not_exists(user)
        self._verify_password(user)
        token = self._generate_token(user)
        response = PostTokenAuthenticateResponseModel(token)
        return response
