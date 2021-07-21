from balance.database.settings import UserAlchemyAdapter
from balance.models.user_models import User

from sqlalchemy.orm import Session


class GetReadUserResponseModel:
    def __init__(self, user: User):
        self.user = user

    def __call__(self):
        return self.user.to_json()


class GetReadUserRequestModel:
    def __init__(self, user_id):
        self.user_id = user_id


class GetReadUserInteractor:
    def __init__(self,
                 request: GetReadUserRequestModel,
                 adapter: Session):
        self.request = request
        self.adapter = adapter

    def _get_user(self):
        return self.adapter.query(User).filter(User.id == self.request.user_id).first()

    def run(self):
        user = self._get_user()
        response = GetReadUserResponseModel(user)
        return response
