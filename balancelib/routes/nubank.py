import uuid
import os

from fastapi import APIRouter
from pynubank import Nubank

from balancelib.requests.nubank_request import (
    RequestSendCodeCertificate,
    RequestAccount
)

from balancelib.interactors.post_generete_code_by_email import (
    PostGenerateCodeByEmailInteractor,
    PostGenerateCodeByEmailRequestModel
)

from balancelib.interactors.post_generate_certificate import (
    PostGenerateCertificateInteractor,
    PostGenerateCertificateRequestModel
)

router = APIRouter()

encrypted_code = str(uuid.uuid4())


class MyClass:
    def __init__(self):
        self.func = None


myClass = MyClass()


def save_certificate(cert, name):
    path = os.path.join(os.getcwd(), name)
    with open(path, 'wb') as cert_file:
        cert_file.write(cert.export())


@router.post('/certificate/code')
def post_generete_code_by_email(user: RequestSendCodeCertificate):
    request = PostGenerateCodeByEmailRequestModel(user)
    interactor = PostGenerateCodeByEmailInteractor(request)

    result = interactor.run()
    myClass.func = interactor._get_instance_certificate()

    return result()


@router.post('/certificate/{code_id}')
def post_generate_certificate(code_id):
    request = PostGenerateCertificateRequestModel(code_id)
    interactor = PostGenerateCertificateInteractor(request, myClass.func)

    result = interactor.run()

    return result()


@router.post('/account')
def account(request: RequestAccount):
    nu = Nubank()
    certificate_path = f'certificate_{request.cpf}.p12'
    refresh_token = nu.authenticate_with_cert(
        cpf=request.cpf,
        password=request.password,
        cert_path=certificate_path
    )

    nu.authenticate_with_refresh_token(refresh_token, certificate_path)
    account_statements = nu.get_account_statements()

    return account_statements
