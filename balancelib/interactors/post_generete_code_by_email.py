import uuid

from balance_nubank.utils.certificate_generator import CertificateGenerator

from balancelib.interactors.response_api_interactor import ResponseSuccess, ResponseError

from database.adapters.bank import BankAlchemyAdapter


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
            bank_code=self.request.bank.code
        )
        if has_user_bank is True:
            raise ResponseError(
                message="Não é possível conectar o mesmo banco",
                status_code=200,
            )

    def _generete_code(self):
        try:
            response = self.certificate.request_code()
            return response
        finally:
            raise ResponseError(
                message="Dados incorretos. Se o erro persistir entre em contato com o técnico!",
                status_code=401,
            )

    def _get_instance_certificate(self):
        return self.certificate

    def run(self):
        self._check_bank_connect()
        send_to = self._generete_code()
        response = PostGenerateCodeByEmailResponseModel(send_to)
        return response
