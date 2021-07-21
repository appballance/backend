from fastapi import APIRouter, Depends

from balancelib.auth import AuthHandler

from sqlalchemy.orm import Session

from balance.schemas.user_schemas import AuthRegister, AuthLogin
from balance.models import user_models
from balance.database.settings import UserAlchemyAdapter, engine

from balancelib.interactors.post_create_user_interactor import \
    (PostCreateUserRequestModel,
     PostCreateUserInteractor)

from balancelib.interactors.get_read_user_interactor import \
    (GetReadUserRequestModel,
     GetReadUserInteractor)

from balancelib.interactors.post_token_authenticate_interactor import \
    (PostTokenAuthenticateRequestModel,
     PostTokenAuthenticateInteractor)


user_models.Base.metadata.create_all(bind=engine)

router = APIRouter()


@router.post('/users')
def post_create_user(user: AuthRegister,
                     adapter: Session = Depends(UserAlchemyAdapter)):
    request = PostCreateUserRequestModel(user)
    interactor = PostCreateUserInteractor(request, adapter)

    result = interactor.run()

    return result()


@router.get('/users')
def get_read_user(user_id: int = Depends(AuthHandler().auth_wrapper),
                  adapter: Session = Depends(UserAlchemyAdapter)):
    request = GetReadUserRequestModel(user_id)
    interactor = GetReadUserInteractor(request, adapter)

    result = interactor.run()

    return result()


@router.post('/auth')
def post_token_authenticate(user: AuthLogin,
                            adapter: Session = Depends(UserAlchemyAdapter)):
    request = PostTokenAuthenticateRequestModel(user)
    interactor = PostTokenAuthenticateInteractor(request, adapter)

    result = interactor.run()

    return result()
