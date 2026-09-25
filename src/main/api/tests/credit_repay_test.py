import pytest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_request_request import CreditRequestRequest
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.requests.credit_repay_requester import CreditRepayRequester
from src.main.api.requests.credit_request_requester import CreditRequestRequester
from src.main.api.requests.login_account_requester import CreateAccountRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs

@pytest.mark.api
class TestCreditRepay:
    # Позитивный сценарий погашения кредита - ОР 200
    def test_credit_repay_valid(self):
        # Позитивный кейс авторизации ADMIN - ОР 200

        # Позитивный сценарий создания User - ОР 200
        create_user_request = CreateUserRequest(username="Max29", password="Pas!sw0rd", role="ROLE_CREDIT_SECRET")

        c_u_response = CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.status_code_200(),
        ).post(create_user_request)

        assert create_user_request.username == c_u_response.username
        assert create_user_request.role == c_u_response.role

        # Использование Requester для создания счёта
        account_response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Max29", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.status_code_201(),
        ).post()

        assert account_response.balance == 0

        # Сохраняем id из тела ответа созданного счёта
        id_account = account_response.id

        # Позитивный сценарий получения кредита - ОР 201
        credit_request_request = CreditRequestRequest(accountId=id_account, amount=5000, termMonths=12)

        credit_request_response = CreditRequestRequester(
            request_spec=RequestSpecs.auth_headers(username="Max29", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.status_code_201(),
        ).post(credit_request_request)

        assert credit_request_response.balance == 5000
        assert credit_request_request.termMonths == credit_request_response.termMonths
        assert credit_request_request.amount == credit_request_response.amount

        # Сохраняем id из тела ответа созданного кредита
        id_credit = credit_request_response.creditId

        # Позитивный сценарий погашения кредита - ОР 200
        credit_repay_request = CreditRepayRequest(creditId = id_credit, accountId=id_account, amount=5000)

        credit_repay_response = CreditRepayRequester(
            request_spec=RequestSpecs.auth_headers(username="Max29", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.status_code_200(),
        ).post(credit_repay_request)

        assert credit_repay_request.amount == credit_repay_response.amountDeposited



    # Негативный сценарий погашения кредита - ОР 422 (Суммы недостаточно)
    def test_credit_repay_invalid_422(self):

        # Позитивный кейс авторизации ADMIN - ОР 200

        # Позитивный сценарий создания User - ОР 200
        create_user_request = CreateUserRequest(username="Max97", password="Pas!sw0rd", role="ROLE_CREDIT_SECRET")

        c_u_response = CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.status_code_200(),
        ).post(create_user_request)

        assert create_user_request.username == c_u_response.username
        assert create_user_request.role == c_u_response.role

        # Использование Requester для создания счёта
        account_response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Max97", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.status_code_201(),
        ).post()

        assert account_response.balance == 0

        # Сохраняем id из тела ответа созданного счёта
        id_account = account_response.id

        # Позитивный сценарий получения кредита - ОР 201
        credit_request_request = CreditRequestRequest(accountId=id_account, amount=7000, termMonths=12)

        credit_request_response = CreditRequestRequester(
            request_spec=RequestSpecs.auth_headers(username="Max97", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.status_code_201(),
        ).post(credit_request_request)

        assert credit_request_request.termMonths == credit_request_response.termMonths
        assert credit_request_request.amount == credit_request_response.amount

        # Сохраняем id из тела ответа созданного кредита
        id_credit = credit_request_response.creditId

        # Негативный сценарий погашения кредита - ОР 422
        credit_repay_request = CreditRepayRequest(creditId=id_credit, accountId=id_account, amount=5000)

        CreditRepayRequester(
            request_spec=RequestSpecs.auth_headers(username="Max97", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.status_code_422(),
        ).post(credit_repay_request)


