import uuid
from fastapi import APIRouter, Depends
from pynubank import Nubank

from balancelib.interactors.authenticate_interactor import (
    AuthenticateInteractor,
)

from balancelib.schemas.nubank_schemas import (
    RequestSendCodeCertificate,
    RequestBank,
)
from balancelib.interactors.post_generete_code_by_email import (
    PostGenerateCodeByEmailInteractor,
    PostGenerateCodeByEmailRequestModel
)
from balancelib.interactors.post_generate_certificate import (
    PostGenerateCertificateInteractor,
    PostGenerateCertificateRequestModel
)

from database.adapters.bank import BankAlchemyAdapter
from database.adapters.user import UserAlchemyAdapter


router = APIRouter()

encrypted_code = str(uuid.uuid4())


class MyClass:
    def __init__(self):
        self.func = None


myClass = MyClass()


@router.post('/nubank/send-email-code')
def post_generete_code_by_email(
        bank: RequestSendCodeCertificate,
        user_id: int = Depends(AuthenticateInteractor().auth_wrapper)):
    request = PostGenerateCodeByEmailRequestModel(bank, user_id)
    interactor = PostGenerateCodeByEmailInteractor(request, BankAlchemyAdapter())

    result = interactor.run()
    myClass.func = interactor._get_instance_certificate()

    return result()


@router.post('/nubank/auth')
def nubank_auth_code(
        bank: RequestBank,
        user_id: int = Depends(AuthenticateInteractor().auth_wrapper)):
    request = PostGenerateCertificateRequestModel(bank, user_id)
    adapter = BankAlchemyAdapter()
    interactor = PostGenerateCertificateInteractor(request, adapter, myClass.func)

    result = interactor.run()

    return result()
