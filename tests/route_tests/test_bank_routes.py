from unittest.mock import patch, MagicMock

from balancelib.routes.bank_routes import get_read_bank

patch_root = 'balancelib.routes.bank_routes'


@patch(f'{patch_root}.Depends')
@patch(f'{patch_root}.AuthenticateInteractor')
@patch(f'{patch_root}.BankAlchemyAdapter')
@patch(f'{patch_root}.GetReadBankRequestModel')
@patch(f'{patch_root}.GetReadBankInteractor')
def test_get_read_bank(mock_get_read_bank_interactor,
                       mock_get_read_bank_request_model,
                       mock_bank_alchemy_adapter,
                       mock_authenticate_interactor,
                       mock_depends):
    mock_entity_id = MagicMock()
    mock_page = MagicMock()
    mock_per_page = MagicMock()
    mock_user_id = mock_depends(mock_authenticate_interactor().auth_wrapper)

    mock_result = get_read_bank(
        mock_entity_id,
        mock_page,
        mock_per_page,
        mock_user_id, )

    mock_get_read_bank_request_model.assert_called_once_with(
        mock_entity_id,
        mock_user_id,
        mock_page,
        mock_per_page, )

    mock_get_read_bank_interactor.assert_called_once_with(
        mock_get_read_bank_request_model(),
        mock_bank_alchemy_adapter())

    mock_get_read_bank_interactor().run.assert_called_once()

    assert mock_result == mock_get_read_bank_interactor().run()()
