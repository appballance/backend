from unittest.mock import MagicMock, patch

from pytest import fixture

from balancelib.interactors.post_token_authenticate_interactor import (
    PostTokenAuthenticateResponseModel,
    PostTokenAuthenticateRequestModel,
    PostTokenAuthenticateInteractor,
)


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

    result = PostTokenAuthenticateResponseModel(mock_token)()

    assert result.get("token") == mock_token


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


def test_post_token_authenticate_interactor_get_user_by_email(interactor_factory):
    interactor = interactor_factory()

    result = interactor._get_user_by_email()

    interactor.adapter.get_by_email.assert_called_once_with(interactor.request.email)

    assert result == interactor.adapter.get_by_email()
