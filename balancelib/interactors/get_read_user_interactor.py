from balancelib.interactors.response_api_interactor import ResponseSuccess

from database.adapters.user import UserAlchemyAdapter
from database.adapters.bank import BankAlchemyAdapter


class GetReadUserResponseModel:
    def __init__(self, user, banks):
        self.user = user
        self.banks = banks

    def __call__(self):
        user = self.user.to_json()
        banks = [bank.to_json() for bank in self.banks]
        return ResponseSuccess({
            'surname': user['surname'],
            'banks': banks
        })


class GetReadUserRequestModel:
    def __init__(self, user_id):
        self.user_id = user_id


class GetReadUserInteractor:
    def __init__(self,
                 request: GetReadUserRequestModel,
                 user_adapter: UserAlchemyAdapter(),
                 bank_adapter: BankAlchemyAdapter()):
        self.request = request
        self.user_adapter = user_adapter
        self.bank_adapter = bank_adapter

    def _get_user(self):
        return self.user_adapter.get_by_id(user_id=self.request.user_id)

    def _get_user_banks(self):
        return self.bank_adapter.get_by_user_id(user_id=self.request.user_id)

    def run(self):
        banks = self._get_user_banks()
        user = self._get_user()
        response = GetReadUserResponseModel(user, banks)
        return response
