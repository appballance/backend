import uuid
from fastapi import APIRouter, Depends


from balancelib.interactors.authenticate_interactor import (
    AuthenticateInteractor,
)

from balancelib.requests.nubank_request import (
    RequestSendCodeCertificate,
)
from balancelib.interactors.post_generete_code_by_email import (
    PostGenerateCodeByEmailInteractor,
    PostGenerateCodeByEmailRequestModel
)
from balancelib.interactors.post_generate_certificate import (
    PostGenerateCertificateInteractor,
    PostGenerateCertificateRequestModel
)

from balance_service.adapters.bank_alchemy_adapter import BankAlchemyAdapter


router = APIRouter()

encrypted_code = str(uuid.uuid4())


class MyClass:
    def __init__(self):
        self.func = None


myClass = MyClass()


@router.post('/nubank/send-email-code')
def post_generete_code_by_email(user: RequestSendCodeCertificate):
    request = PostGenerateCodeByEmailRequestModel(user)
    interactor = PostGenerateCodeByEmailInteractor(request)

    result = interactor.run()
    myClass.func = interactor._get_instance_certificate()

    return result()


@router.post('/nubank/auth/{code_id}')
def nubank_auth_code(
        code_id,
        user_id: int = Depends(AuthenticateInteractor().auth_wrapper)):
    request = PostGenerateCertificateRequestModel(code_id, user_id)
    adapter = BankAlchemyAdapter()
    interactor = PostGenerateCertificateInteractor(request, adapter, myClass.func)

    result = interactor.run()

    return result()
