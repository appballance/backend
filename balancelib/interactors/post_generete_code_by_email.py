import uuid
from pynubank.utils.certificate_generator import CertificateGenerator

from balancelib.interactors.response_api_interactor import ResponseSuccess


class PostGenerateCodeByEmailResponseModel:
    def __init__(self, send_to):
        self.send_to = send_to

    def __call__(self):
        return ResponseSuccess({
            "email": self.send_to,
        })


class PostGenerateCodeByEmailRequestModel:
    def __init__(self, user):
        self.cpf = user.cpf
        self.password = user.password
        self.device_id = user.device_id
        self.encrypted_code = str(uuid.uuid4())  # alert


class PostGenerateCodeByEmailInteractor:
    def __init__(self, request):
        self.request = request
        self.certificate = CertificateGenerator(
            login=self.request.cpf,
            password=self.request.password,
            device_id=self.request.device_id,
            encrypted_code=self.request.encrypted_code
        )

    def _generete_code(self):
        return self.certificate.request_code()

    def _get_instance_certificate(self):
        return self.certificate

    def run(self):
        send_to = self._generete_code()
        response = PostGenerateCodeByEmailResponseModel(send_to)
        return response
