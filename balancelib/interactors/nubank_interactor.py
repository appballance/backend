import os
import zipfile

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
            interactor_service=BotoS3Interactor()
        )

        bucket_certificates = os.environ['BUCKET_CERTIFICATES']
        bucket_fastapi = os.environ['BUCKET_FASTAPI']

        has_file = s3.has_file(
            bucket_path=bucket_certificates,
            file_path=certificate_url)

        if has_file:
            # s3.download_file(bucket_fastapi, 'api.zip', 'api.zip')
            s3.download_file(bucket_certificates, certificate_url, certificate_url)
            return True
            # with zipfile.ZipFile('api.zip', mode='a') as package:
            #     package.write(certificate_url, arcname=certificate_url)

            # s3.upload_file(bucket_fastapi, 'api.zip', 'api.zip')
            # os.remove('api.zip')
            # os.remove(certificate_url)

        return False

    def authenticate(self,
                     token: str,
                     certificate_path: str) -> str:
        return self.service.authenticate_with_refresh_token(
            token,
            certificate_path)

    def has_certificate(self, certificate_url):
        is_file = os.path.isfile(certificate_url)

        if is_file:
            return True

        has_in_s3 = self._get_certificate_in_bucket(certificate_url)
        return has_in_s3

    def get_balance(self):
        return self.service.get_account_balance()

    def get_transactions(self) -> list:
        return self.service.get_account_statements()
