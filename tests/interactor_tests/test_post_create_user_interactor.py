from unittest.mock import MagicMock, patch

from pytest import fixture

from balancelib.interactors.post_create_user_interactor import (
    PostCreateUserResponseModel,
    PostCreateUserRequestModel,
    PostCreateUserInteractor)


@fixture
def interactor_factory():
    def request_interactor(mock_request=MagicMock(),
                           mock_adapter=MagicMock()):
        return PostCreateUserInteractor(mock_request,
                                        mock_adapter)
    return request_interactor


def test_post_create_user_response_model():
    mock_user = MagicMock()

    result = PostCreateUserResponseModel(mock_user)

    assert result.user == mock_user


def test_post_create_user_response_model_call():
    mock_user = MagicMock()

    result = PostCreateUserResponseModel(mock_user)()

    mock_user.to_json.assert_called_once_with()

    assert result == mock_user.to_json()


def test_post_create_user_request_model():
    mock_user = MagicMock()

    result = PostCreateUserRequestModel(mock_user)

    assert result.surname == mock_user.surname
    assert result.fullname == mock_user.fullname
    assert result.email == mock_user.email
    assert result.password1 == mock_user.password1
    assert result.password2 == mock_user.password2


def test_post_create_user_interactor(interactor_factory):
    mock_request = MagicMock()
    mock_adapter = MagicMock()

    interactor = interactor_factory(mock_request, mock_adapter)

    assert interactor.request == mock_request
    assert interactor.adapter == mock_adapter


def test_post_create_user_interactor_get_user_by_email(interactor_factory):
    interactor = interactor_factory()

    result = interactor._get_user_by_email()

    mock_user = interactor.adapter.query().filter().first()

    assert result == mock_user


patch_root = 'balancelib.interactors.post_create_user_interactor'


@patch(f'{patch_root}.User')
@patch(f'{patch_root}.AuthenticateInteractor')
def test_post_create_user_interactor_create_user(mock_auth,
                                                 mock_function_user,
                                                 interactor_factory):
    interactor = interactor_factory()

    result = interactor._create_user()

    mock_auth().get_password_hash(interactor.request.password1)

    mock_user = mock_function_user(surname=interactor.request.surname,
                                   fullname=interactor.request.fullname,
                                   email=interactor.request.email,
                                   hashed_password=interactor.request.
                                   hashed_password,)

    interactor.adapter.add(mock_user)
    interactor.adapter.commit()
    interactor.adapter.refresh(mock_user)

    assert result == mock_user


@patch.object(PostCreateUserInteractor, '_get_user_by_email')
@patch(f'{patch_root}.PostCreateUserResponseModel')
def test_post_create_user_interactor_run(mock_response,
                                         mock_get_user_by_email,
                                         interactor_factory):
    interactor = interactor_factory()

    # result = interactor.run()

    mock_get_user_by_email.assert_called_once_with()
