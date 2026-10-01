import pytest
from api.classes.api_manager import ApiManager
from api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_request_request import CreditRequestRequest


@pytest.mark.api
class TestCreditRequest:
    # Позитивный сценарий получения кредита - ОР 201
    def test_credit_request_valid(self, api_manager: ApiManager, create_user_request_credit):
        acc = api_manager.user_steps.create_account(create_user_request_credit)
        id_account = acc.id

        credit_request = CreditRequestRequest(accountId=id_account, amount=5000, termMonths=12)

        response = api_manager.user_steps.credit_request(credit_request, create_user_request_credit)

        assert response.amount == credit_request.amount
        assert response.termMonths == credit_request.termMonths



    # Негативный сценарий получения кредита - ОР 404
    def test_credit_request_invalid_404(self, api_manager: ApiManager, create_user_request_credit: CreateUserRequest):
        acc = api_manager.user_steps.create_account(create_user_request_credit)
        id_account = acc.id

        credit_request_one = CreditRequestRequest(accountId=id_account, amount=5000, termMonths=12)
        api_manager.user_steps.credit_request(credit_request_one, create_user_request_credit)

        credit_request_two = CreditRequestRequest(accountId=id_account, amount=5000, termMonths=12)
        api_manager.user_steps.credit_request_invalid_404(credit_request_two, create_user_request_credit)




