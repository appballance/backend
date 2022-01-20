from balance_domain.models.user_models import User

from fastapi import HTTPException

from balancelib.interactors.authenticate_interactor import \
    AuthenticateInteractor


class PostCreateUserResponseModel:
    def __init__(self, user: User):
        self.user = user

    def __call__(self):
        return self.user.to_json()


class PostCreateUserRequestModel:
    def __init__(self, user):
        self.surname = user.surname
        self.fullname = user.fullname
        self.email = user.email
        self.password1 = user.password1
        self.password2 = user.password2


class PostCreateUserInteractor:
    def __init__(self, request, adapter):
        self.request = request
        self.adapter = adapter

    def _get_user_by_email(self):
        return self.adapter.query(User).filter(
            User.email == self.request.email).first()

    def _check_user_exists(self):
        user = self._get_user_by_email()
        if user:
            raise HTTPException(status_code=400,
                                detail="Email already registered")

    def _password_match(self):
        if self.request.password1.lower() != \
                self.request.password2.lower():
            raise HTTPException(status_code=400,
                                detail="Password doesn't match")

    def _create_user(self):
        hashed_password = AuthenticateInteractor().\
            get_password_hash(self.request.password1)

        user = User(surname=self.request.surname,
                    fullname=self.request.fullname,
                    email=self.request.email,
                    hashed_password=hashed_password,)
        self.adapter.add(user)
        self.adapter.commit()
        self.adapter.refresh(user)
        return user

    def run(self):
        self._check_user_exists()
        self._password_match()
        user = self._create_user()
        response = PostCreateUserResponseModel(user)
        return response
