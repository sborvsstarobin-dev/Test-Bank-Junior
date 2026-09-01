import pytest
import requests

from src.main.api.models.auth_login_request import AuthLoginRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.auth_login_response import AuthLoginResponse
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
# Позитивный сценарий создания User - ОР 200
class TestCreateUser:

    def test_create_user_valid(self):

        # Позитивный кейс авторизации ADMIN - ОР 200

        # Позитивный сценарий создания User - ОР 200
        create_user_request = CreateUserRequest(username = "Max140", password = "Pas!sw0rd", role = "ROLE_USER")

        c_u_response = CreateUserRequester(
            request_spec = RequestSpecs.auth_headers(username = "admin", password = "123456"),
            response_spec= ResponseSpecs.status_code_200(),
        ).post(create_user_request)

        assert create_user_request.username == c_u_response.username
        assert create_user_request.role == c_u_response.role


    @pytest.mark.parametrize(
        "username,password",
        [ ("Саша", "Pas!sw0rd"), # Негативный сценарий, кириллица в логине - ОР 400
          ("ad", "Pas!sw0rd"),  # Негативный сценарий, меньше 3 символов в логине - ОР 400
          ("adminadminadminadmin", "Pas!sw0rd"),  # Негативный сценарий, больше 15 символов в логине - ОР 400
          ("admin!", "Pas!sw0rd"),  # Негативный сценарий, спецсимволы в логине - ОР 400
          ("admin", "фPas!sфw0rd"),  # Негативный сценарий, кириллица в пароле - ОР 400
          ("admin", "Pas!sw0"),  # Негативный сценарий, меньше 8 символов в пароле - ОР 400
          ("admin", "pas!sw0rd"),  # Негативный сценарий, без заглавных букв в пароле - ОР 400
          ("admin", "PAS!SWORD"),  # Негативный сценарий, без маленьких букв в пароле - ОР 400
          ("admin", "Passsw0rd"),  # Негативный сценарий, без спецсимволов в пароле - ОР 400
          ("admin", "Pas!sword")  # Негативный сценарий, без цифр в пароле - ОР 400
        ]
    )


    # Негативный сценарий создания User - ОР 400
    def test_create_user_invalid_400(self, username, password):
        # Позитивный кейс авторизации ADMIN - ОР 200
        auth_admin_request = AuthLoginRequest(username = "admin", password = "123456")

        auth_admin_response = requests.post(
            url = "http://localhost:4111/api/auth/token/login",
            json = auth_admin_request.model_dump(),
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        )
        # Проверка на статус код
        assert auth_admin_response.status_code == 200

        auth_login_response = AuthLoginResponse(**auth_admin_response.json())
        assert auth_admin_request.username == auth_login_response.user.username
        assert auth_login_response.user.role == "ROLE_ADMIN"

        token = auth_admin_response.json().get("token")

        # Негативный сценарий создания User - ОР 400
        create_user_request = CreateUserRequest(username = username, password = password, role = "ROLE_USER")

        create_user_response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json = create_user_request.model_dump(),
            headers = {
                "Content-Type": "application/json",
                "Accept": "*/*",
                "Authorization": f"Bearer {token}"
            }
        )
        assert create_user_response.status_code == 400


# Негативный сценарий создания User - ОР 401
    def test_create_user_invalid_401(self):
        # Позитивный кейс авторизации ADMIN - ОР 200
        auth_admin_request = AuthLoginRequest(username = "admin", password = "123456")

        auth_admin_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json = auth_admin_request.model_dump(),
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        )
        # Проверка на статус код
        assert auth_admin_response.status_code == 200

        auth_login_response = AuthLoginResponse(**auth_admin_response.json())
        assert auth_admin_request.username == auth_login_response.user.username
        assert auth_login_response.user.role == "ROLE_ADMIN"

        token = auth_admin_response.json().get("token")

        # Негативный сценарий создания User - ОР 401
        create_user_request = CreateUserRequest(username = "Max140", password = "Pas!sw0rd", role = "ROLE_USER")

        create_user_response = requests.post(
            url = "http://localhost:4111/api/admin/create",
            json = create_user_request.model_dump(),
            headers={
                "Content-Type": "application/json",
                "Accept": "*/*",
                "Authorization": f"Bearer"
            }
        )
        assert create_user_response.status_code == 401