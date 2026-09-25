import pytest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.requests.login_account_requester import CreateAccountRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api

class TestCreateAccount:
    # Позитивный сценарий создания ACCOUNT - ОР 201
    def test_create_account_valid(self):
        # Позитивный кейс авторизации ADMIN - ОР 200

        # Позитивный сценарий создания User - ОР 200
        create_user_request = CreateUserRequest(username="Max140", password="Pas!sw0rd", role="ROLE_USER")

        c_u_response = CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.status_code_200(),
        ).post(create_user_request)

        assert create_user_request.username == c_u_response.username
        assert create_user_request.role == c_u_response.role

        # Использование Requester для создания счёта
        account_response = CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="Max140", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.status_code_201(),
        ).post()

        assert account_response.balance == 0




    # Негативный сценарий создания ACCOUNT - ОР 403 (Создание под Админом)
    def test_create_account_invalid_403(self):
        # Использование Requester для создания счёта
        CreateAccountRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.status_code_403(),
        ).post()