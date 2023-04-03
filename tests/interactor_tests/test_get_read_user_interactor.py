from unittest.mock import MagicMock, patch

from pytest import fixture

from balancelib.interactors.get_read_user_interactor import (
    GetReadUserResponseModel,
    GetReadUserRequestModel,
    GetReadUserInteractor
)


@fixture
def interactor_factory():
    def request_interactor(mock_request=MagicMock(),
                           mock_user_adapter=MagicMock(),
                           mock_bank_adapter=MagicMock()):
        return GetReadUserInteractor(mock_request,
                                     mock_user_adapter,
                                     mock_bank_adapter)

    return request_interactor


def test_get_read_user_response_model():
    mock_surname = MagicMock()
    mock_balance = MagicMock()
    mock_banks = MagicMock()

    response = GetReadUserResponseModel(mock_surname, mock_balance, mock_banks)

    assert response.surname == mock_surname
    assert response.user_balance == mock_balance
    assert response.banks == mock_banks


def test_get_read_user_response_model_call():
    mock_surname = MagicMock()
    mock_balance = MagicMock()
    mock_banks = MagicMock()

    result = GetReadUserResponseModel(mock_surname, mock_balance, mock_banks)()

    assert result.get('surname') == mock_surname
    assert result.get('balance') == mock_balance
    assert result.get('banks') == mock_banks


def test_get_read_user_request_model():
    mock_user_id = MagicMock()

    response = GetReadUserRequestModel(mock_user_id)

    assert response.user_id == mock_user_id


def test_get_read_user_interactor(interactor_factory):
    mock_request = MagicMock()
    mock_user_adapter = MagicMock()
    mock_bank_adapter = MagicMock()

    interactor = interactor_factory(mock_request,
                                    mock_user_adapter,
                                    mock_bank_adapter, )

    assert interactor.request == mock_request
    assert interactor.user_adapter == mock_user_adapter
    assert interactor.bank_adapter == mock_bank_adapter


patch_root = 'balancelib.interactors.get_read_user_interactor'


def test_get_read_user_interactor_get_user(interactor_factory):
    interactor = interactor_factory()

    result = interactor._get_user()

    mock_user = interactor.user_adapter.get_by_id()

    assert result == mock_user


@patch.object(GetReadUserInteractor, '_get_user_banks_formatted')
@patch.object(GetReadUserInteractor, '_get_user')
@patch(f'{patch_root}.GetReadUserResponseModel')
def test_get_read_user_interactor_run(mock_response,
                                      mock_get_user,
                                      mock_get_user_banks_formatted,
                                      interactor_factory):
    interactor = interactor_factory()

    result = interactor.run()

    mock_get_user.assert_called_once_with()
    mock_get_user_banks_formatted.assert_called_once_with()
    mock_response.assert_called_once_with(
        surname=interactor._get_user().surname,
        user_balance=interactor.user_balance,
        banks=interactor._get_user_banks_formatted(),
    )

    assert result == mock_response()
