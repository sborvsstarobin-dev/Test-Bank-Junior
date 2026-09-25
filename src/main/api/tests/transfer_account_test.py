import pytest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.models.transfer_account_request import TransferAccountRequest
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.requests.deposit_account_requester import DepositAccountRequester
from src.main.api.requests.login_account_requester import CreateAccountRequester
from src.main.api.requests.transfer_account_requester import TransferAccountRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs

@pytest.mark.api
class TestTransferAccount:
    # Позитивный сценарий перевода счёта - ОР 200
    def test_transfer_account_valid(self):
        # Позитивный кейс авторизации ADMIN - ОР 200

        # Позитивный сценарий создания User - ОР 200
        create_user_request = CreateUserRequest(username="Max551", password="Pas!sw0rd", role="ROLE_USER")

        c_u_response = CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.status_code_200(),
        ).post(create_user_request)

        assert create_user_request.username == c_u_response.username
        assert create_user_request.role == c_u_response.role

        # Использование Requester для создания счёта

        # Позитивный сценарий создания ACCOUNT  №1 - ОР 201
        account_response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Max551", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.status_code_201(),
        ).post()

        # Проверка баланса
        assert account_response.balance == 0

        # Сохраняем id из тела ответа созданного счёта
        id_account_1 = account_response.id

        # Позитивный сценарий создания ACCOUNT  №2 - ОР 201
        account_response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Max551", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.status_code_201(),
        ).post()

        # Проверка баланса
        assert account_response.balance == 0

        # Сохраняем id из тела ответа созданного счёта
        id_account_2 = account_response.id

        # Позитивный сценарий пополнения счета - ОР 200
        deposit_account_request = DepositAccountRequest(accountId=id_account_1, amount="4000.5")

        deposit_account_response = DepositAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Max551", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.status_code_200(),
        ).post(deposit_account_request)

        # Проверка счёта на балансе
        assert deposit_account_response.balance == 4000.5

        # Позитивный сценарий перевода - ОР 200
        transfer_account_request = TransferAccountRequest(fromAccountId=id_account_1, toAccountId=id_account_2, amount="570.5")

        transfer_account_response = TransferAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Max551", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.status_code_200(),
        ).post(transfer_account_request)

        assert transfer_account_response.toAccountId == id_account_2
        assert transfer_account_response.fromAccountId == id_account_1


    # Негативный сценарий перевода счёта - ОР 401(Пользователь не авторизован)
    def test_transfer_account_invalid_401(self):
        # Позитивный кейс авторизации ADMIN - ОР 200

        # Позитивный сценарий создания User - ОР 200
        create_user_request = CreateUserRequest(username="Max153", password="Pas!sw0rd", role="ROLE_USER")

        c_u_response = CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.status_code_200(),
        ).post(create_user_request)

        assert create_user_request.username == c_u_response.username
        assert create_user_request.role == c_u_response.role

        # Использование Requester для создания счёта

        # Позитивный сценарий создания ACCOUNT  №1 - ОР 201
        account_response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Max153", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.status_code_201(),
        ).post()

        # Проверка баланса
        assert account_response.balance == 0

        # Сохраняем id из тела ответа созданного счёта
        id_account_1 = account_response.id

        # Позитивный сценарий создания ACCOUNT  №2 - ОР 201
        account_response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Max153", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.status_code_201(),
        ).post()

        # Проверка баланса
        assert account_response.balance == 0

        # Сохраняем id из тела ответа созданного счёта
        id_account_2 = account_response.id

        # Позитивный сценарий пополнения счета - ОР 200
        deposit_account_request = DepositAccountRequest(accountId=id_account_1, amount="4000.5")

        deposit_account_response = DepositAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Max153", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.status_code_200(),
        ).post(deposit_account_request)

        # Проверка счёта на балансе
        assert deposit_account_response.balance == 4000.5

        # Негативный сценарий перевода - ОР 401
        transfer_account_request = TransferAccountRequest(fromAccountId=id_account_1, toAccountId=id_account_2, amount="570.5")

        transfer_account_response = TransferAccountRequester(
            request_spec=RequestSpecs.no_auth_headers(),
            response_spec=ResponseSpecs.status_code_401(),
        ).post(transfer_account_request)










