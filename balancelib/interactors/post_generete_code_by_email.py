import uuid
from pynubank.utils.certificate_generator import CertificateGenerator


class PostGenerateCodeByEmailResponseModel:
    def __init__(self, certificate):
        self.certificate = certificate

    def __call__(self):
        return self.certificate


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
        self.certificate.request_code()

    def _get_instance_certificate(self):
        return self.certificate

    def run(self):
        self._generete_code()
        response = PostGenerateCodeByEmailResponseModel({
            "status_code": 201,
            "message": "success",
        })
        return response
