import pytest
from api.classes.api_manager import ApiManager
from api.fixtures.user_fixture import transfer_account_request_invalid_401
from src.main.api.models.transfer_account_request import TransferAccountRequest


@pytest.mark.api
class TestTransferAccount:
    # Позитивный сценарий перевода счёта - ОР 200
    def test_transfer_account_valid(self, api_manager: ApiManager, transfer_account_request: TransferAccountRequest):
        create_user_req, deposit_account_req, transfer_account_req, id_account_one, id_account_two = transfer_account_request
        response = api_manager.user_steps.transfer_account(create_user_req, transfer_account_req)

        assert response.fromAccountId == transfer_account_req.fromAccountId
        assert response.toAccountId == transfer_account_req.toAccountId
        expected_balance = deposit_account_req.amount - transfer_account_req.amount
        assert response.fromAccountIdBalance == expected_balance


    # Негативный сценарий перевода счёта - ОР 401(Пользователь не авторизован)
    def test_transfer_account_invalid_401(self, api_manager: ApiManager, transfer_account_request_invalid_401):
        deposit_account_req, transfer_account_req, id_account_one, id_account_two = transfer_account_request_invalid_401
        api_manager.user_steps.transfer_account_invalid_401(transfer_account_req)












