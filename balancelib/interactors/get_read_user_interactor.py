from database.adapters.user import UserAlchemyAdapter
from database.adapters.bank import BankAlchemyAdapter

from balancelib.interactors.nubank_interactor import NuBankInteractor
from balancelib.interactors.response_api_interactor import ResponseSuccess, ResponseError
from balancelib.interactors.get_read_bank_interactor import (
    BasicBankResponseModel
)

from balance_service.interfaces.nubank import (
    NuBankServiceInterface,
)

from balance_domain.entities.bank import BankEntity


class GetReadUserResponseModel:
    def __init__(self, surname, user_balance: int, banks: list):
        self.surname = surname
        self.user_balance = user_balance
        self.banks = banks

    def __call__(self):
        return ResponseSuccess({
            'surname': self.surname,
            'balance': self.user_balance,
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
        self.user_balance = 0

    def _get_user(self):
        return self.user_adapter.get_by_id(user_id=self.request.user_id)

    def _get_user_banks(self):
        return self.bank_adapter.get_by_user_id(user_id=self.request.user_id)

    @staticmethod
    def get_nubank_instance(token: str,
                            certificate_path: str):
        return NuBankServiceInterface(
            token=token,
            certificate_path=certificate_path,
            bank_service=NuBankInteractor()
        )

    def _enriched_bank_nubank(self, bank: BankEntity) -> dict:
        try:
            nubank_instance = self.get_nubank_instance(
                token=bank.token,
                certificate_path=bank.certificate_url, )

            new_bank = BasicBankResponseModel(
                entity_id=bank.id,
                balance=nubank_instance.get_balance(),
                code=bank.code
            )
            return new_bank.to_json()
        except:
            raise ResponseError(status_code=400,
                                message="Nubank failed instance")

    def _get_user_banks_formatted(self):
        banks = []

        for bank in self._get_user_banks():
            new_bank = self._enriched_bank_nubank(bank)

            if new_bank is not None:
                self.user_balance += new_bank.get('balance')
                banks.append(new_bank)

        return banks

    def run(self):
        user = self._get_user()
        banks = self._get_user_banks_formatted()

        response = GetReadUserResponseModel(
            surname=user.surname,
            user_balance=self.user_balance,
            banks=banks
        )
        return response
