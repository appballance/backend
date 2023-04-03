from balancelib.schemas.user_schemas import AuthLogin
from balance_domain.entities.user import UserEntity

from database.adapters.user import UserAlchemyAdapter

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
                 adapter: UserAlchemyAdapter()):
        self.request = request
        self.adapter = adapter

    def _get_user_by_email(self):
        return self.adapter.get_by_email(self.request.email)

    @staticmethod
    def _check_user_not_exists(user: UserEntity):
        if user is None:
            raise ResponseError(
                message="Email ou senha incorreto",
                status_code=400,
            )

    def _verify_password(self, user: UserEntity):
        if not AuthenticateInteractor().verify_password(
                self.request.password,
                user.password):
            raise ResponseError(
                message="Email ou senha incorretod",
                status_code=400,
            )

    @staticmethod
    def _generate_token(user: UserEntity):
        token = AuthenticateInteractor().encode_token(user.id)
        return token

    def run(self):
        user = self._get_user_by_email()
        self._check_user_not_exists(user)
        self._verify_password(user)
        token = self._generate_token(user)
        response = PostTokenAuthenticateResponseModel(token)
        return response
