from unittest.mock import MagicMock, patch

from pytest import fixture

from balancelib.interactors import (
    PostTokenAuthenticateResponseModel,
    PostTokenAuthenticateRequestModel,
    PostTokenAuthenticateInteractor,)


@fixture
def interactor_factory():
    def request_interactor(mock_request=MagicMock(),
                           mock_adapter=MagicMock()):
        return PostTokenAuthenticateInteractor(mock_request, mock_adapter)
    return request_interactor


def test_post_token_authenticate_response_model():
    mock_token = MagicMock()

    result = PostTokenAuthenticateResponseModel(mock_token)

    assert result.token == mock_token


def test_post_token_authenticate_response_model_call():
    mock_token = MagicMock()

    result = PostTokenAuthenticateResponseModel(mock_token)

    assert result() == mock_token


def test_post_token_authenticate_request_model():
    mock_user = MagicMock()

    result = PostTokenAuthenticateRequestModel(mock_user)

    assert result.email == mock_user.email
    assert result.password == mock_user.password


def test_post_token_authenticate_interactor():
    mock_request = MagicMock()
    mock_adapter = MagicMock()

    interactor = PostTokenAuthenticateInteractor(mock_request, mock_adapter)

    assert interactor.request == mock_request
    assert interactor.adapter == mock_adapter


patch_root = 'balancelib.interactors.post_token_authenticate_interactor'


@patch(f'{patch_root}.User')
def test_post_token_authenticate_interactor_get_user_by_email(
        mock_user,
        interactor_factory):
    interactor = interactor_factory()

    result = interactor._get_user_by_email()

    interactor.adapter.query.assert_called_once_with(mock_user)
    interactor.adapter.query().filter.assert_called_once_with(False)
    interactor.adapter.query().filter().first.assert_called_once()

    assert result == interactor.adapter.query(mock_user).filter(False).first()
