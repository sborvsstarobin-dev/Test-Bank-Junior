import pytest

from src.main.api.models.auth_login_request import AuthLoginRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.requests.login_user_requester import LoginUserRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs

@pytest.mark.api

class TestAuthAdmin:
    # Позитивный кейс авторизации ADMIN - ОР 200
    def test_auth_admin_valid(self):
        # Позитивный кейс авторизации ADMIN - ОР 200
        auth_admin_request = AuthLoginRequest(username = "admin", password = "123456")

        auth_admin_response = LoginUserRequester(
            request_spec=RequestSpecs.no_auth_headers(),
            response_spec = ResponseSpecs.status_code_200(),
        ).post(auth_admin_request)

        # Проверка на имя и роль
        assert auth_admin_request.username == auth_admin_response.user.username
        assert auth_admin_response.user.role == "ROLE_ADMIN"


    @pytest.mark.parametrize(
        "username,password",
        [
            ("", "123456"),  # Отсутствует логин - ОР 400
            ("admin", "")    # Отсутствует пароль - ОР 400
        ]
    )

    # Негативный кейс авторизации ADMIN - ОР 400
    def test_auth_admin_invalid_400(self, username, password):
        auth_admin_request = AuthLoginRequest(username = username, password = password)

        LoginUserRequester(
            request_spec=RequestSpecs.no_auth_headers(),
            response_spec=ResponseSpecs.status_code_400(),
        ).post(auth_admin_request)



    @pytest.mark.parametrize(
        "username,password",
        [
            ("kldndf", "123456"),  # Неправильный логин - ОР 401
            ("admin", "dsfsf33")  # Неправильный пароль - ОР 401
        ]
    )
    # Негативный кейс авторизации ADMIN - ОР 401
    def test_auth_admin_invalid_401(self, username, password):
        auth_admin_request = AuthLoginRequest(username = username, password = password)

        LoginUserRequester(
            request_spec=RequestSpecs.no_auth_headers(),
            response_spec=ResponseSpecs.status_code_401(),
        ).post(auth_admin_request)








    # Позитивный кейс авторизации USER - ОР 200
    def test_auth_user_valid(self):
        create_user_request = CreateUserRequest(username="Max140", password="Pas!sw0rd", role="ROLE_USER")

        c_u_response = CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.status_code_200(),
        ).post(create_user_request)

        assert create_user_request.username == c_u_response.username
        assert create_user_request.role == c_u_response.role

        # Позитивный кейс авторизации USER - ОР 200
        auth_admin_request = AuthLoginRequest(username = "Max140", password = "Pas!sw0rd")

        auth_admin_response = LoginUserRequester(
            request_spec=RequestSpecs.no_auth_headers(),
            response_spec=ResponseSpecs.status_code_200(),
        ).post(auth_admin_request)

        # Проверка на имя и роль
        assert auth_admin_request.username == auth_admin_response.user.username
        assert auth_admin_response.user.role == "ROLE_USER"

    # Негативный кейс авторизации USER - ОР 401 (Некорректный пароль)
    def test_auth_user_invalid_401(self):
        # Позитивный кейс авторизации ADMIN - ОР 200
        create_user_request = CreateUserRequest(username="Max14", password="Pas!sw0rd", role="ROLE_USER")

        c_u_response = CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.status_code_200(),
        ).post(create_user_request)

        assert create_user_request.username == c_u_response.username
        assert create_user_request.role == c_u_response.role

        # Негативный кейс авторизации USER - ОР 401
        auth_admin_request = AuthLoginRequest(username="Max14", password="Pas!sw0r")

        LoginUserRequester(
            request_spec=RequestSpecs.no_auth_headers(),
            response_spec=ResponseSpecs.status_code_401(),
        ).post(auth_admin_request)

