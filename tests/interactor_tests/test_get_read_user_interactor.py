from unittest.mock import MagicMock, patch

from pytest import fixture

from balancelib.interactors.get_read_user_interactor import \
    (GetReadUserResponseModel,
     GetReadUserRequestModel,
     GetReadUserInteractor)


@fixture
def interactor_factory():
    def request_interactor(mock_request=MagicMock(),
                           mock_adapter=MagicMock()):
        return GetReadUserInteractor(mock_request,
                                     mock_adapter)
    return request_interactor


def test_get_read_user_response_model():
    mock_user = MagicMock()

    response = GetReadUserResponseModel(mock_user)

    assert response.user == mock_user


def test_get_read_user_response_model_call():
    mock_user = MagicMock()

    result = GetReadUserResponseModel(mock_user)()

    mock_user.to_json.assert_called_once_with()

    assert result == mock_user.to_json()


def test_get_read_user_request_model():
    mock_user_id = MagicMock()

    response = GetReadUserRequestModel(mock_user_id)

    assert response.user_id == mock_user_id


def test_get_read_user_interactor(interactor_factory):
    mock_request = MagicMock()
    mock_adapter = MagicMock()

    interactor = interactor_factory(mock_request, mock_adapter)

    assert interactor.request == mock_request
    assert interactor.adapter == mock_adapter


patch_root = 'balancelib.interactors.get_read_user_interactor'


def test_get_read_user_interactor_get_user(interactor_factory):
    interactor = interactor_factory()

    result = interactor._get_user()

    mock_user = interactor.adapter.query().filter().first()

    assert result == mock_user


@patch.object(GetReadUserInteractor, '_get_user')
@patch(f'{patch_root}.GetReadUserResponseModel')
def test_get_read_user_interactor_run(mock_response,
                                      mock_get_user,
                                      interactor_factory):
    interactor = interactor_factory()

    result = interactor.run()

    mock_get_user.assert_called_once_with()
    mock_response.assert_called_once_with(interactor._get_user())

    assert result == mock_response()
