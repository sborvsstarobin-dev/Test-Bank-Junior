import pytest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.requests.deposit_account_requester import DepositAccountRequester
from src.main.api.requests.login_account_requester import CreateAccountRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs

@pytest.mark.api
class TestDepositAccount:
    # Позитивный сценарий пополнения счёта - ОР 200
    def test_deposit_account_valid(self):
        # Позитивный кейс авторизации ADMIN - ОР 200

        # Позитивный сценарий создания User - ОР 200
        create_user_request = CreateUserRequest(username="Max13", password="Pas!sw0rd", role="ROLE_USER")

        c_u_response = CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.status_code_200(),
        ).post(create_user_request)

        assert create_user_request.username == c_u_response.username
        assert create_user_request.role == c_u_response.role

        # Использование Requester для создания счёта
        account_response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Max13", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.status_code_201(),
        ).post()

        # Проверка баланса
        assert account_response.balance == 0

        # Сохраняем id из тела ответа созданного счёта
        id_account = account_response.id

        # Позитивный сценарий пополнения счета - ОР 200
        deposit_account_request = DepositAccountRequest(accountId = id_account, amount = "1000.5")

        deposit_account_response = DepositAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Max13", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.status_code_200(),
        ).post(deposit_account_request)

        # Проверка счёта на балансе
        assert deposit_account_response.balance == 1000.5




    # Негативный сценарий пополнения счёта - ОР 400 (Некорректное тело запроса)
    def test_deposit_account_invalid_400(self):
        # Позитивный кейс авторизации ADMIN - ОР 200

        # Позитивный сценарий создания User - ОР 200
        create_user_request = CreateUserRequest(username="Max15", password="Pas!sw0rd", role="ROLE_USER")

        c_u_response = CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.status_code_200(),
        ).post(create_user_request)

        assert create_user_request.username == c_u_response.username
        assert create_user_request.role == c_u_response.role

        # Использование Requester для создания счёта
        account_response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Max15", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.status_code_201(),
        ).post()

        # Проверка баланса
        assert account_response.balance == 0

        # Сохраняем id из тела ответа созданного счёта
        id_account = account_response.id

        # Негативный сценарий пополнения счета - ОР 400
        deposit_account_request = DepositAccountRequest(accountId=id_account, amount="-3")

        DepositAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Max15", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.status_code_400(),
        ).post(deposit_account_request)




    # Негативный сценарий пополнения счёта - ОР 401 (Пользователь не авторизован)
    def test_deposit_account_invalid_401(self):
        # Позитивный кейс авторизации ADMIN - ОР 200

        # Позитивный сценарий создания User - ОР 200
        create_user_request = CreateUserRequest(username="Max47", password="Pas!sw0rd", role="ROLE_USER")

        c_u_response = CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.status_code_200(),
        ).post(create_user_request)

        assert create_user_request.username == c_u_response.username
        assert create_user_request.role == c_u_response.role

        # Использование Requester для создания счёта
        account_response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Max47", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.status_code_201(),
        ).post()

        # Проверка баланса
        assert account_response.balance == 0

        # Сохраняем id из тела ответа созданного счёта
        id_account = account_response.id

        # Негативный сценарий пополнения счета - ОР 401
        deposit_account_request = DepositAccountRequest(accountId=id_account, amount="1000.5")

        DepositAccountRequester(
            request_spec=RequestSpecs.no_auth_headers(),
            response_spec=ResponseSpecs.status_code_401(),
        ).post(deposit_account_request)



