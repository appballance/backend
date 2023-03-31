from unittest.mock import patch

from balancelib import (post_create_user,
                        get_read_user,
                        post_token_authenticate)

patch_root = 'balancelib.routes.user_routes'


@patch(f'{patch_root}.AuthRegister')
@patch(f'{patch_root}.Depends')
@patch(f'{patch_root}.UserAlchemyAdapter')
@patch(f'{patch_root}.PostCreateUserRequestModel')
@patch(f'{patch_root}.PostCreateUserInteractor')
def test_post_create_user(mock_post_create_user_interactor,
                          mock_post_create_user_request_model,
                          mock_user_alchemy_adapter,
                          mock_depends,
                          mock_auth_register):
    result = post_create_user(mock_auth_register,
                              mock_depends(mock_user_alchemy_adapter))

    mock_post_create_user_request_model.assert_called_once_with(
        mock_auth_register)

    mock_post_create_user_interactor.assert_called_once_with(
        mock_post_create_user_request_model(),
        mock_depends(mock_user_alchemy_adapter))

    mock_post_create_user_interactor().run.assert_called_once()

    assert result == mock_post_create_user_interactor().run()()


@patch(f'{patch_root}.Depends')
@patch(f'{patch_root}.AuthenticateInteractor')
@patch(f'{patch_root}.UserAlchemyAdapter')
@patch(f'{patch_root}.GetReadUserRequestModel')
@patch(f'{patch_root}.GetReadUserInteractor')
def test_get_read_user(mock_get_read_user_interactor,
                       mock_get_read_user_request_model,
                       mock_user_alchemy_adapter,
                       mock_authenticate_interactor,
                       mock_depends):
    user_id = mock_depends(mock_authenticate_interactor().auth_wrapper)
    adapter = mock_depends(mock_user_alchemy_adapter)

    result = get_read_user(user_id, adapter)

    mock_get_read_user_request_model.assert_called_once_with(user_id)

    mock_get_read_user_interactor.assert_called_once_with(
        mock_get_read_user_request_model(), adapter)

    mock_get_read_user_interactor().run.assert_called_once()

    assert result == mock_get_read_user_interactor().run()()


@patch(f'{patch_root}.AuthLogin')
@patch(f'{patch_root}.Depends')
@patch(f'{patch_root}.UserAlchemyAdapter')
@patch(f'{patch_root}.PostTokenAuthenticateRequestModel')
@patch(f'{patch_root}.PostTokenAuthenticateInteractor')
def test_post_token_authenticate(mock_post_token_authenticate_interactor,
                                 mock_post_token_authenticate_request_model,
                                 mock_user_alchemy_adapter,
                                 mock_depends,
                                 mock_auth_login):
    adapter = mock_depends(mock_user_alchemy_adapter)

    result = post_token_authenticate(mock_auth_login, adapter)

    mock_post_token_authenticate_request_model.assert_called_once_with(
        mock_auth_login)

    mock_post_token_authenticate_interactor.assert_called_once_with(
        mock_post_token_authenticate_request_model(),
        adapter)

    mock_post_token_authenticate_interactor().run.assert_called_once()

    assert result == mock_post_token_authenticate_interactor().run()()
