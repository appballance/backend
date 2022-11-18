from sqlalchemy.orm import Session

from balance_domain.database.settings import UserAlchemyAdapter
from balance_domain.models.user_models import User, Bank

from balancelib.interactors.response_api_interactor import ResponseSuccess


class GetReadUserResponseModel:
    def __init__(self, user: User, banks: list):
        self.user = user
        self.banks = banks

    def __call__(self):
        user = self.user.to_json()
        return ResponseSuccess({
            'surname': user['surname'],
            'banks': self.banks
        })


class GetReadUserRequestModel:
    def __init__(self, user_id):
        self.user_id = user_id


class GetReadUserInteractor:
    def __init__(self,
                 request: GetReadUserRequestModel,
                 adapter: Session(UserAlchemyAdapter)):
        self.request = request
        self.adapter = adapter

    def _get_user(self):
        return self.adapter.query(User). \
            filter(User.id == self.request.user_id).first()

    def _get_user_banks(self):
        return self.adapter.query(Bank). \
            filter(Bank.user_id == self.request.user_id).all()

    def run(self):
        banks = [bank.to_json() for bank in self._get_user_banks()]
        user = self._get_user()
        response = GetReadUserResponseModel(user, banks)
        return response
