import pytest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_request_request import CreditRequestRequest
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.requests.credit_request_requester import CreditRequestRequester
from src.main.api.requests.login_account_requester import CreateAccountRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs

@pytest.mark.api
class TestCreditRequest:
    # Позитивный сценарий получения кредита - ОР 201
    def test_credit_request_valid(self):
        # Позитивный кейс авторизации ADMIN - ОР 200

        # Позитивный сценарий создания User - ОР 200
        create_user_request = CreateUserRequest(username="Max34", password="Pas!sw0rd", role="ROLE_CREDIT_SECRET")

        c_u_response = CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.status_code_200(),
        ).post(create_user_request)

        assert create_user_request.username == c_u_response.username
        assert create_user_request.role == c_u_response.role

        # Использование Requester для создания счёта
        account_response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Max34", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.status_code_201(),
        ).post()

        assert account_response.balance == 0

        # Сохраняем id из тела ответа созданного счёта
        id_account = account_response.id

        # Позитивный сценарий получения кредита - ОР 201
        credit_request_request = CreditRequestRequest(accountId = id_account, amount = 5000, termMonths = 12)

        credit_request_response = CreditRequestRequester(
            request_spec=RequestSpecs.auth_headers(username="Max34", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.status_code_201(),
        ).post(credit_request_request)

        assert credit_request_response.balance == 5000
        assert credit_request_request.termMonths == credit_request_response.termMonths
        assert credit_request_request.amount == credit_request_response.amount




    # Негативный сценарий получения кредита - ОР 404
    def test_credit_request_invalid_404(self):
        # Позитивный кейс авторизации ADMIN - ОР 200

        # Позитивный сценарий создания User - ОР 200
        create_user_request = CreateUserRequest(username="Max247", password="Pas!sw0rd", role="ROLE_CREDIT_SECRET")

        c_u_response = CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.status_code_200(),
        ).post(create_user_request)

        assert create_user_request.username == c_u_response.username
        assert create_user_request.role == c_u_response.role

        # Использование Requester для создания счёта
        account_response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Max247", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.status_code_201(),
        ).post()

        assert account_response.balance == 0

        # Сохраняем id из тела ответа созданного счёта
        id_account = account_response.id

        # Позитивный сценарий получения кредита - ОР 201
        credit_request_request = CreditRequestRequest(accountId=id_account, amount=5000, termMonths=12)

        credit_request_response = CreditRequestRequester(
            request_spec=RequestSpecs.auth_headers(username="Max247", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.status_code_201(),
        ).post(credit_request_request)

        # Негативный сценарий получения кредита - ОР 404
        credit_request_request = CreditRequestRequest(accountId=id_account, amount=5000, termMonths=12)

        CreditRequestRequester(
            request_spec=RequestSpecs.auth_headers(username="Max247", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.status_code_404(),
        ).post(credit_request_request)




