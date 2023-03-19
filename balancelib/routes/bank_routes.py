from fastapi import APIRouter, Depends

from balancelib.interactors.authenticate_interactor import AuthenticateInteractor
from balancelib.interactors.get_read_bank_interactor import (
    GetReadBankRequestModel,
    GetReadBankInteractor
)

from database.adapters.bank import BankAlchemyAdapter

router = APIRouter()


@router.get('/bank/{entity_id}')
def get_read_bank(
        entity_id: int,
        page: int,
        per_page: int,
        user_id: str = Depends(AuthenticateInteractor().auth_wrapper)):
    request = GetReadBankRequestModel(
        entity_id,
        user_id,
        page,
        per_page,
    )
    interactor = GetReadBankInteractor(request, BankAlchemyAdapter())

    result = interactor.run()

    return result()
