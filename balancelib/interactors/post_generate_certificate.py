import uuid
import os

from fastapi import HTTPException
from pynubank.utils.certificate_generator import CertificateGenerator


class PostGenerateCertificateResponseModel:
    def __init__(self, certificate):
        self.certificate = certificate

    def __call__(self):
        return self.certificate


class PostGenerateCertificateRequestModel:
    def __init__(self, code_id):
        self.encrypted_code = str(uuid.uuid4())  # alert
        self.code_id = code_id


class PostGenerateCertificateInteractor:
    def __init__(self, request, certificate):
        self.request = request
        self.certificate = certificate
        self.certificate_path = f'certificate_{certificate.login}.p12'

    def _check_code_exists(self):
        if self.certificate is None:
            raise HTTPException(status_code=400,
                                detail="Generate the code of certificate first")

    def _get_certificate(self):
        self.cert1, _ = self.certificate.exchange_certs(
            code=self.request.code_id
        )
        return self.cert1

    def _save_certificate(self, certificate):
        path = os.path.join(os.getcwd(), self.certificate_path)
        with open(path, 'wb') as cert_file:
            cert_file.write(certificate.export())

    def run(self):
        self._check_code_exists()
        certificate = self._get_certificate()
        self._save_certificate(certificate)
        response = PostGenerateCertificateResponseModel({
            "status_code": 201,
            "message": "success",
        })
        return response
