from unittest.mock import patch

from balancelib.routes.nubank_routes import (
    post_generete_code_by_email,
    nubank_auth_code,
)


patch_root = 'balancelib.routes.nubank_routes'


@patch(f'{patch_root}.RequestSendCodeCertificate')
@patch(f'{patch_root}.Depends')
@patch(f'{patch_root}.AuthenticateInteractor')
@patch(f'{patch_root}.BankAlchemyAdapter')
@patch(f'{patch_root}.PostGenerateCodeByEmailRequestModel')
@patch(f'{patch_root}.PostGenerateCodeByEmailInteractor')
def test_post_generate_code_by_email(
        mock_post_generate_code_by_email_interactor,
        mock_post_generate_code_by_email_request_model,
        mock_bank_alchemy_adapter,
        mock_authenticate_interactor,
        mock_depends,
        mock_bank):
    mock_user_id = mock_depends(mock_authenticate_interactor().auth_wrapper)

    mock_result = post_generete_code_by_email(
        mock_bank,
        mock_user_id,
    )

    mock_post_generate_code_by_email_request_model.assert_called_once_with(
        mock_bank,
        mock_user_id,
    )

    mock_post_generate_code_by_email_interactor.assert_called_once_with(
        mock_post_generate_code_by_email_request_model(),
        mock_bank_alchemy_adapter(),
    )

    assert mock_result == mock_post_generate_code_by_email_interactor().run()()


@patch(f'{patch_root}.RequestBank')
@patch(f'{patch_root}.Depends')
@patch(f'{patch_root}.AuthenticateInteractor')
# @patch(f'{patch_root}.BankAlchemyAdapter')
@patch(f'{patch_root}.PostGenerateCertificateRequestModel')
@patch(f'{patch_root}.PostGenerateCertificateInteractor')
def test_post_nubank_auth_code(
        mock_post_generate_certificate_interactor,
        mock_post_generate_certificate_request_model,
        # mock_bank_alchemy_adapter,
        mock_authenticate_interactor,
        mock_depends,
        mock_bank, ):
    mock_user_id = mock_depends(mock_authenticate_interactor().auth_wrapper)

    mock_result = nubank_auth_code(
        mock_bank,
        mock_user_id,
    )

    mock_post_generate_certificate_request_model.assert_called_once_with(
        mock_bank,
        mock_user_id,
    )

    # mock_post_generate_certificate_interactor.assert_called_once_with(
    #     mock_post_generate_certificate_request_model(),
    #     mock_bank_alchemy_adapter(),
    # )

    assert mock_result == mock_post_generate_certificate_interactor().run()()
