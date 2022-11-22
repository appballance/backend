import uuid
from pynubank.utils.certificate_generator import CertificateGenerator

from balancelib.interactors.response_api_interactor import ResponseSuccess, ResponseError

from balance_service.adapters.bank_alchemy_adapter import BankAlchemyAdapter


class PostGenerateCodeByEmailResponseModel:
    def __init__(self, send_to):
        self.send_to = send_to

    def __call__(self):
        return ResponseSuccess({
            "email": self.send_to,
        })


class PostGenerateCodeByEmailRequestModel:
    def __init__(self, bank, user_id):
        self.bank = bank
        self.user_id = user_id
        self.encrypted_code = str(uuid.uuid4())  # alert


class PostGenerateCodeByEmailInteractor:
    def __init__(self,
                 request: PostGenerateCodeByEmailRequestModel,
                 adapter: BankAlchemyAdapter()):
        self.adapter = adapter
        self.request = request
        self.certificate = CertificateGenerator(
            login=self.request.bank.cpf,
            password=self.request.bank.password,
            device_id=self.request.bank.device_id,
            encrypted_code=self.request.encrypted_code
        )

    def _check_bank_connect(self):
        has_user_bank = self.adapter.user_has_bank(
            user_id=self.request.user_id,
            bank_number=self.request.bank.number
        )
        if has_user_bank is True:
            raise ResponseError(
                message="This user are connect with this bank",
                status_code=400,
            )

    def _generete_code(self):
        return self.certificate.request_code()

    def _get_instance_certificate(self):
        return self.certificate

    def run(self):
        self._check_bank_connect()
        send_to = self._generete_code()
        response = PostGenerateCodeByEmailResponseModel(send_to)
        return response
