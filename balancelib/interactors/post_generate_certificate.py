import os
import uuid

# move to service ?
from pynubank import Nubank
from pynubank.utils.certificate_generator import CertificateGenerator

from database.adapters.bank import BankAlchemyAdapter

from balancelib.interactors.response_api_interactor import (
    ResponseSuccess,
    ResponseError
)

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

    def _check_send_code_by_email(self):
        if self.certificate is None:
            raise ResponseError(status_code=400,
                                message="Generate the code of certificate first")
        self.cpf = self.certificate.login
        self.password = self.certificate.password

    def _get_certificate(self):
        self.cert1, _ = self.certificate.exchange_certs(
            code=self.request.bank.code_id
        )
        return self.cert1

    @staticmethod
    def _save_certificate(certificate_file,
                          certificate_path):
        path = os.path.join(os.getcwd(), certificate_path)
        with open(path, 'wb') as cert_file:
            cert_file.write(certificate_file.export())

    def _get_token_nubank(self, certificate_path):
        nu = Nubank()
        token_nubank = nu.authenticate_with_cert(
            cpf=self.cpf,
            password=self.password,
            cert_path=certificate_path
        )
        return token_nubank

    def _conect_with_nubank(self, token_nubank):
        bank_entity = BankEntity(
            token=token_nubank,
            number=self.request.bank.number,
            user_id=self.request.user_id,
        )
        bank = self.adapter.create(bank_entity)
        return bank

    def run(self):
        self._check_send_code_by_email()

        certificate_path = f'certificate_{self.request.user_id}.p12'
        certificate_file = self._get_certificate()

        self._save_certificate(certificate_file, certificate_path)

        token_nubank = self._get_token_nubank(certificate_path)

        bank = self._conect_with_nubank(token_nubank)

        response = PostGenerateCertificateResponseModel(bank)
        return response
