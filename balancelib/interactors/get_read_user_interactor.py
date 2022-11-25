import os

import boto3
from balance_service.interfaces.boto_s3 import BotoS3
from pynubank import Nubank

from balancelib.interactors.boto_s3_interactor import BotoS3Interactor
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

    def has_certificate(self, certificate_path):
        is_file = os.path.isfile(certificate_path)
        if is_file:
            return True
        return False

    def get_balance(self):
        return self.service.get_account_balance()


class BankResponse:
    def __init__(self,
                 balance: int,
                 code: str):
        self.balance = balance
        self.code = code

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

    def _get_certificate_in_bucket(self, certificate_url):
        s3 = BotoS3(interactor_service=BotoS3Interactor())

        has_file = s3.has_file(file_path=certificate_url)

        if has_file:
            s3.download_file(file_path=certificate_url,
                             file_path_new=certificate_url)

    def run(self):
        user = self._get_user()
        banks = []

        for bank in self._get_user_banks():
            self._get_certificate_in_bucket(bank.certificate_url)

            balance = self._get_nubank_balance(
                bank_token=bank.token,
                certificate_path=bank.certificate_url,)

            new_bank = BankResponse(
                balance=balance,
                code=bank.code,)

            banks.append(new_bank)

        response = GetReadUserResponseModel(user, banks)
        return response
