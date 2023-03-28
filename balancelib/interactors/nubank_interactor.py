import os
from cachetools import cached, TTLCache

from balance_nubank import Nubank

from balance_service.interfaces.boto_s3 import BotoS3
from balance_service.interfaces.nubank import (
    NuBankServiceBasicInterface,
)

from balancelib.interactors.boto_s3_interactor import BotoS3Interactor


class NuBankInteractor(NuBankServiceBasicInterface):
    def __init__(self):
        self.service = Nubank()

    @staticmethod
    @cached(cache=TTLCache(maxsize=100, ttl=3600))
    def _get_certificate_in_bucket(certificate_url: str) -> bool:
        s3 = BotoS3(
            interactor_service=BotoS3Interactor(
                bucket_name=os.environ['BUCKET_CERTIFICATES']
            )
        )

        has_file = s3.has_file(file_path=certificate_url)

        if has_file:
            s3.download_file(file_path=certificate_url,
                             file_path_new=certificate_url)
            return True
        return False

    def authenticate(self,
                     token: str,
                     certificate_path: str) -> str:
        return self.service.authenticate_with_refresh_token(
            token,
            certificate_path)

    def has_certificate(self, certificate_path):
        is_file = os.path.isfile(certificate_path)

        if is_file:
            return True

        has_in_s3 = self._get_certificate_in_bucket(
            certificate_url=certificate_path
        )
        return has_in_s3

    def get_balance(self):
        return self.service.get_account_balance()

    def get_transactions(self) -> list:
        return self.service.get_account_statements()
