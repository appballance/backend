import os

from database.adapters.user import UserAlchemyAdapter
from database.adapters.bank import BankAlchemyAdapter

from balancelib.interactors.boto_s3_interactor import BotoS3Interactor
from balancelib.interactors.nubank_interactor import NuBankInteractor
from balancelib.interactors.response_api_interactor import ResponseSuccess
from balancelib.interactors.get_read_bank_interactor import (
    BasicBankResponseModel,
    BasicTransactionResponse
)

from balance_service.interfaces.boto_s3 import BotoS3
from balance_service.interfaces.nubank import (
    NuBankServiceInterface,
)

from balance_domain.entities.bank import BankEntity


class GetReadUserResponseModel:
    def __init__(self, user, user_balance: int, banks: list):
        self.user = user
        self.user_balance = user_balance
        self.banks = banks

    def __call__(self):
        user = self.user.to_json()
        return ResponseSuccess({
            'surname': user['surname'],
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

    def _get_user(self):
        return self.user_adapter.get_by_id(user_id=self.request.user_id)

    def _get_user_banks(self):
        return self.bank_adapter.get_by_user_id(user_id=self.request.user_id)

    @staticmethod
    def _get_nubank(bank_token: str,
                    certificate_path: str):
        return NuBankServiceInterface(
            token=bank_token,
            certificate_path=certificate_path,
            bank_service=NuBankInteractor()
        )

    @staticmethod
    def _get_certificate_in_bucket(certificate_url: str):
        s3 = BotoS3(
            interactor_service=BotoS3Interactor(
                bucket_name=os.environ['BUCKET_CERTIFICATES']
            )
        )

        has_file = s3.has_file(file_path=certificate_url)

        if has_file:
            s3.download_file(file_path=certificate_url,
                             file_path_new=certificate_url)

    def _mount_bank_nubank(self, bank: BankEntity) -> dict:
        self._get_certificate_in_bucket(
            bank.certificate_url
        )

        nubank_instance = self._get_nubank(
            bank_token=bank.token,
            certificate_path=bank.certificate_url, )

        new_bank = BasicBankResponseModel(
            entity_id=bank.id,
            balance=nubank_instance.get_balance(),
            code=bank.code
        )
        return new_bank.to_json()

    def run(self):
        user = self._get_user()
        banks = []
        user_balance = 0

        for bank in self._get_user_banks():
            new_bank = self._mount_bank_nubank(bank)

            if new_bank is None:
                user_balance = 0
            else:
                user_balance = new_bank.get('balance')

            banks.append(new_bank)

        response = GetReadUserResponseModel(user, user_balance, banks)
        return response
