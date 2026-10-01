import pytest
from api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest

@pytest.mark.api
class TestDepositAccount:
    # Позитивный сценарий пополнения счёта - ОР 200
    def test_deposit_account_valid(self, api_manager: ApiManager,deposit_account_request):
        create_user_req, create_account_req, deposit_account_req = deposit_account_request
        response = api_manager.user_steps.deposit_account(create_user_req, deposit_account_req)

        assert response.balance == deposit_account_req.amount


    # Негативный сценарий пополнения счёта - ОР 400 (Некорректное тело запроса)
    def test_deposit_account_invalid_400(self, api_manager: ApiManager,deposit_account_request_invalid_400):
        create_user_req, create_account_req, deposit_account_req = deposit_account_request_invalid_400
        api_manager.user_steps.deposit_account_invalid_400(create_user_req, deposit_account_req)



    # Негативный сценарий пополнения счёта - ОР 401 (Пользователь не авторизован)
    def test_deposit_account_invalid_401(self, api_manager: ApiManager, create_user_request: CreateUserRequest, deposit_account_request_invalid_401):
        deposit_account_req = deposit_account_request_invalid_401
        api_manager.user_steps.deposit_account_invalid_401(deposit_account_req)



