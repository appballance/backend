from sqlalchemy.orm import Session

from balance_domain.schemas.user_schemas import AuthLogin
from balance_domain.models.user_models import User

from balancelib.interactors.authenticate_interactor import (
    AuthenticateInteractor,
)

from balancelib.interactors.response_api_interactor import (
    ResponseError,
    ResponseSuccess,
)


class PostTokenAuthenticateResponseModel:
    def __init__(self, token):
        self.token = token

    def __call__(self):
        return ResponseSuccess({
            "token": self.token
        })


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
            raise ResponseError(message="Invalid email/password", status_code=401)

    def _verify_password(self, user: User):
        if not AuthenticateInteractor().verify_password(
                self.request.password,
                user.hashed_password):
            raise ResponseError(message="Invalid email/password", status_code=401)

    @staticmethod
    def _generate_token(user: User):
        token = AuthenticateInteractor().encode_token(user.id)
        return token

    def run(self):
        user = self._get_user_by_email()
        self._check_user_not_exists(user)
        self._verify_password(user)
        token = self._generate_token(user)
        response = PostTokenAuthenticateResponseModel(token)
        return response
