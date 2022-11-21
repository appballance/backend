from fastapi import APIRouter, Depends

from balancelib.interactors.authenticate_interactor import (
    AuthenticateInteractor,
)

from balancelib.interactors.post_create_user_interactor import (
    PostCreateUserRequestModel,
    PostCreateUserInteractor
)

from balancelib.interactors.get_read_user_interactor import (
    GetReadUserRequestModel,
    GetReadUserInteractor,
)

from balancelib.interactors.post_token_authenticate_interactor import (
    PostTokenAuthenticateRequestModel,
    PostTokenAuthenticateInteractor,
)

from balancelib.schemas.user_schemas import (
    AuthRegister,
    AuthLogin,
)

from balance_service.adapters.user_alchemy_adapter import UserAlchemyAdapter
from balance_service.adapters.bank_alchemy_adapter import BankAlchemyAdapter


router = APIRouter()


@router.post('/user')
def post_create_user(user: AuthRegister):
    request = PostCreateUserRequestModel(user)
    interactor = PostCreateUserInteractor(request, UserAlchemyAdapter())

    result = interactor.run()

    return result()


@router.get('/user')
def get_read_user(
        user_id: int = Depends(AuthenticateInteractor().auth_wrapper)):
    request = GetReadUserRequestModel(user_id)
    interactor = GetReadUserInteractor(request, UserAlchemyAdapter(), BankAlchemyAdapter())

    result = interactor.run()

    return result()


@router.post('/auth')
def post_token_authenticate(user: AuthLogin):
    request = PostTokenAuthenticateRequestModel(user)
    interactor = PostTokenAuthenticateInteractor(request, UserAlchemyAdapter())

    result = interactor.run()

    return result()
