import pytest
import requests

from src.main.api.models.auth_login_request import AuthLoginRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.auth_login_response import AuthLoginResponse
from src.main.api.models.create_user_response import CreateUserResponse

@pytest.mark.api
# Позитивный кейс авторизации USER - ОР 200
class TestCreateUser:

    def test_auth_login_valid(self):
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

        # Позитивный сценарий создания User - ОР 200
        create_user_request = CreateUserRequest(username = "Max140", password = "Pas!sw0rd", role = "ROLE_USER")

        c_u_response = requests.post(
            url = "http://localhost:4111/api/admin/create",
            json = create_user_request.model_dump(),
            headers = {
                "Content-Type": "application/json",
                "Accept": "*/*",
                "Authorization": f"Bearer {token}"
            }
        )
        assert c_u_response.status_code == 200

        create_user_response = CreateUserResponse(**c_u_response.json())
        assert create_user_request.username == create_user_response.username
        assert create_user_request.role == create_user_response.role

        # Позитивный кейс авторизации USER - ОР 200
        auth_user_request = AuthLoginRequest(username = "Max140", password = "Pas!sw0rd")

        auth_user_response = requests.post(
            url = "http://localhost:4111/api/auth/token/login",
            json = auth_user_request.model_dump(),
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        )
        # Проверка на статус код
        assert auth_user_response.status_code == 200

        auth_login_response = AuthLoginResponse(**auth_user_response.json())
        assert auth_user_request.username == auth_login_response.user.username
        assert auth_login_response.user.role == "ROLE_USER"


    @pytest.mark.parametrize(
        "username,password",
        [
            ("Max140", "")  # Отсутствует пароль - ОР 400
        ]
    )

    # Негативный кейс авторизации USER - ОР 400
    def test_auth_user_invalid_username_400(self, username, password):
        # Позитивный кейс авторизации ADMIN - ОР 200
        auth_admin_request = AuthLoginRequest(username="admin", password="123456")

        auth_admin_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json=auth_admin_request.model_dump(),
            headers={
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

        # Позитивный сценарий создания User - ОР 200
        create_user_request = CreateUserRequest(username="Max140", password="Pas!sw0rd", role="ROLE_USER")

        c_u_response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json=create_user_request.model_dump(),
            headers={
                "Content-Type": "application/json",
                "Accept": "*/*",
                "Authorization": f"Bearer {token}"
            }
        )
        assert c_u_response.status_code == 200

        create_user_response = CreateUserResponse(**c_u_response.json())
        assert create_user_request.username == create_user_response.username
        assert create_user_request.role == create_user_response.role

        # Негативный кейс авторизации USER - ОР 400
        auth_user_request = AuthLoginRequest(username=username, password=password)

        auth_user_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json=auth_user_request.model_dump(),
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        )
        # Проверка на статус код
        assert auth_user_response.status_code == 400



    @pytest.mark.parametrize(
        "username,password",
        [
            ("123323", "Pas!sw0rd")  # Неправильный логин - ОР 401
        ]
    )

    # Негативный кейс авторизации USER - ОР 401
    def test_auth_user_invalid_username_401(self, username, password):
        # Позитивный кейс авторизации ADMIN - ОР 200
        auth_admin_request = AuthLoginRequest(username="admin", password="123456")

        auth_admin_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json=auth_admin_request.model_dump(),
            headers={
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

        # Позитивный сценарий создания User - ОР 200
        create_user_request = CreateUserRequest(username="Max140", password="Pas!sw0rd", role="ROLE_USER")

        c_u_response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json=create_user_request.model_dump(),
            headers={
                "Content-Type": "application/json",
                "Accept": "*/*",
                "Authorization": f"Bearer {token}"
            }
        )
        assert c_u_response.status_code == 200

        create_user_response = CreateUserResponse(**c_u_response.json())
        assert create_user_request.username == create_user_response.username
        assert create_user_request.role == create_user_response.role



        # Негативный кейс авторизации USER - ОР 401
        auth_user_request = AuthLoginRequest(username=username, password=password)

        auth_user_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json=auth_user_request.model_dump(),
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        )
        # Проверка на статус код
        assert auth_user_response.status_code == 401