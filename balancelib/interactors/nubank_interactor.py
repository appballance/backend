import os
import boto3

from pynubank import Nubank

from balance_service.interfaces.boto_s3 import BotoS3
from balance_service.interfaces.nubank import (
    NuBankServiceBasicInterface,
)


from balancelib.interactors.boto_s3_interactor import (
    BotoS3Interactor,
    BotoS3RequestModel, )


class NuBankInteractor(NuBankServiceBasicInterface):
    def __init__(self):
        self.service = Nubank()
        self.folder_certificates = os.environ['FOLDER_TEMPORARY']
        self.bucket_certificates = os.environ['BUCKET_CERTIFICATES']

    def _get_certificate_in_bucket(self, certificate_url: str) -> bool:
        request = BotoS3RequestModel(
            region_name=os.environ['AWS_S3_REGION_NAME'],
            aws_access_key_id=os.environ['AWS_S3_KEY_ID'],
            aws_secret_access_key=os.environ['AWS_S3_KEY'],
        )
        instance = BotoS3(
            interactor_service=BotoS3Interactor(
                request=request,
                service=boto3,
            )
        )

        has_file = instance.has_file(
            bucket_name=self.bucket_certificates,
            file_path=certificate_url)

        if has_file:
            instance.download_file(
                bucket_name=self.bucket_certificates,
                file_path=certificate_url,
                file_path_new=f'{self.folder_certificates}/{certificate_url}',)

            if os.path.isfile(
                    f'{self.folder_certificates}/{certificate_url}'):
                print(
                    f'WARNING: File {certificate_url} in directory '
                    f'"{self.folder_certificates}" created with success')
                return True
            else:
                print(f'ERROR: File {certificate_url} dont created')
                return False

        return False

    def authenticate(self,
                     token: str,
                     certificate_path: str) -> str:
        return self.service.authenticate_with_refresh_token(
            token,
            f'{self.folder_certificates}/{certificate_path}')

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
