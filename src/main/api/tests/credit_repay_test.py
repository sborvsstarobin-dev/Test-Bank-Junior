import pytest
from api.classes.api_manager import ApiManager
from src.main.api.models.credit_repay_request import CreditRepayRequest


@pytest.mark.api
class TestCreditRepay:
    # Позитивный сценарий погашения кредита - ОР 200
    def test_credit_repay_valid(self, api_manager: ApiManager, credit_repay_request):
        create_user_req, credit_request_req, credit_repay_req, id_credit = credit_repay_request

        response = api_manager.user_steps.credit_repay(credit_repay_req, create_user_req)

        assert response.amountDeposited == credit_repay_req.amount
        assert credit_repay_req.creditId == id_credit

    # Негативный сценарий погашения кредита - ОР 422 (Суммы недостаточно)
    def test_credit_repay_invalid_422(self, api_manager: ApiManager, credit_repay_request_invalid_422):
        create_user_req, credit_request_req, credit_repay_req, id_credit = credit_repay_request_invalid_422

        api_manager.user_steps.credit_repay_invalid_422(credit_repay_req, create_user_req)