from pynubank import Nubank

from database.adapters.user import UserAlchemyAdapter
from database.adapters.bank import BankAlchemyAdapter

from balancelib.interactors.response_api_interactor import ResponseSuccess

from balance_service.interfaces.nubank import (
    NuBankServiceBasicInterface,
    NuBankServiceInterface,
)


class NuBankService(NuBankServiceBasicInterface):
    def __init__(self):
        self.service = Nubank()

    def authenticate(self,
                     token: str,
                     certificate_path: str):
        return self.service.authenticate_with_refresh_token(
            token,
            certificate_path)

    def get_balance(self):
        return self.service.get_account_balance()


class BankResponse:
    def __init__(self, balance):
        self.balance = balance

    def to_json(self):
        vars(self)


class GetReadUserResponseModel:
    def __init__(self, user, banks):
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
                 user_adapter: UserAlchemyAdapter(),
                 bank_adapter: BankAlchemyAdapter()):
        self.request = request
        self.user_adapter = user_adapter
        self.bank_adapter = bank_adapter

    def _get_user(self):
        return self.user_adapter.get_by_id(user_id=self.request.user_id)

    def _get_user_banks(self):
        return self.bank_adapter.get_by_user_id(user_id=self.request.user_id)

    def _get_nubank_balance(self,
                            bank_token: str,
                            certificate_path: str):
        nu = NuBankServiceInterface(
            token=bank_token,
            certificate_path=certificate_path,
            bank_service=NuBankService()
        )
        return nu.get_balance()

    def run(self):
        user = self._get_user()

        cert_path = f"certificate_{user.id}.p12"
        banks = [
            BankResponse(
                balance=self._get_nubank_balance(bank_token=bank.token, certificate_path=cert_path),
            ) for bank in self._get_user_banks()]

        response = GetReadUserResponseModel(user, banks)
        return response
