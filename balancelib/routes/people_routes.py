from fastapi import APIRouter, Depends

from balancelib.interactors.post_create_user_interactor import \
    (PostCreateUserRequestModel,
     PostCreateUserInteractor)


from balance.schemas.people_schemas import AuthRegister, AuthLogin
from balance.models import people_models
from balance.database.people import get_db, engine

people_models.Base.metadata.create_all(bind=engine)

router = APIRouter()


@router.post('/users')
def post_create_user(user: AuthRegister, adapter=Depends(get_db)):
    request = PostCreateUserRequestModel(user)
    interactor = PostCreateUserInteractor(request, adapter)

    result = interactor.run()

    return result()


# @router.get("/users")
# def get_read_users(db: Session = Depends(get_db), user_id: int = Depends(auth_handler.auth_wrapper)):
#     return get_user(db, user_id)
#
#
# @router.post("/auth")
# def post_token_authenticate(typed: AuthLogin, db: Session = Depends(get_db)) -> dict:
#     user = get_user_by_email(db, email=typed.email)
#     if user is None:
#         raise HTTPException(status_code=401, detail="Invalid email/password")
#     if not auth_handler.verify_password(typed.password, user.hashed_password):
#         raise HTTPException(status_code=401, detail="Invalid email/password")
#     token = auth_handler.encode_token(user.id)
#     return {
#         "token": token
#     }
