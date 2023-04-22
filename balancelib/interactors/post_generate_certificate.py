import os
import uuid

from dotenv import load_dotenv
from balance_nubank import Nubank
from balance_nubank.utils.certificate_generator import CertificateGenerator

from database.adapters.bank import BankAlchemyAdapter

from balancelib.interactors.boto_s3_interactor import (
    BotoS3Interactor,
)

from balancelib.interactors.response_api_interactor import (
    ResponseSuccess,
    ResponseError
)

from balance_service.interfaces.boto_s3 import BotoS3

from balance_domain.entities.bank import BankEntity


class PostGenerateCertificateResponseModel:
    def __init__(self, bank):
        self.bank = bank

    def __call__(self):
        return ResponseSuccess(self.bank.to_json())


class PostGenerateCertificateRequestModel:
    def __init__(self, bank, user_id):
        self.encrypted_code = str(uuid.uuid4())  # alert
        self.bank = bank
        self.user_id = user_id


class PostGenerateCertificateInteractor:
    def __init__(self,
                 request: PostGenerateCertificateRequestModel,
                 adapter: BankAlchemyAdapter(),
                 certificate: CertificateGenerator):
        self.request = request
        self.adapter = adapter
        self.certificate = certificate
        self.folder_certificates = os.environ['FOLDER_TEMPORARY']
        self.certificate_filename = \
            f'certificate_{self.request.user_id}.p12'
        self.certificate_path = \
            f'{self.folder_certificates}/{self.certificate_filename}'

    def _check_send_code_by_email(self):
        if self.certificate is None:
            raise ResponseError(
                status_code=400,
                message="Generate the code of certificate first"
            )
        self.cpf = self.certificate.login
        self.password = self.certificate.password

    def _get_certificate(self):
        self.cert1, _ = self.certificate.exchange_certs(
            code=self.request.bank.code_id
        )
        return self.cert1

    def _save_certificate(self, certificate_file):
        load_dotenv()
        path = os.path.join(
            os.getcwd(),
            self.certificate_path)

        with open(path, 'wb') as cert_file:
            cert_file.write(certificate_file.export())

        s3 = BotoS3(
            interactor_service=BotoS3Interactor()
        )

        has_file = s3.has_file(
            bucket_path=os.environ['BUCKET_CERTIFICATES'],
            file_path=self.certificate_filename,
        )

        if not has_file:
            s3.upload_file(
                bucket_path=os.environ['BUCKET_CERTIFICATES'],
                file_path=self.certificate_filename,
                file_path_new=self.certificate_path,
            )

    def _get_token_nubank(self, certificate_path):
        nu = Nubank()
        token_nubank = nu.authenticate_with_cert(
            cpf=self.cpf,
            password=self.password,
            cert_path=certificate_path
        )
        return token_nubank

    def _connect_with_nubank(self,
                             token_nubank: str,
                             certificate_url: str):
        bank_entity = BankEntity(
            token=token_nubank,
            code=self.request.bank.code,
            user_id=self.request.user_id,
            certificate_url=certificate_url,
        )
        bank = self.adapter.create(bank_entity)
        return bank

    def run(self):
        self._check_send_code_by_email()

        self._save_certificate(
            self._get_certificate()
        )

        token_nubank = self._get_token_nubank(self.certificate_path)

        bank = self._connect_with_nubank(
            token_nubank,
            self.certificate_filename)

        response = PostGenerateCertificateResponseModel(bank)
        return response
