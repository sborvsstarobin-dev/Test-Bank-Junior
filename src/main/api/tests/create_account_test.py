import pytest
import requests

from src.main.api.models.auth_login_request import AuthLoginRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.auth_login_response import AuthLoginResponse
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.models.create_account_response import CreateAccountResponse

@pytest.mark.api
# Позитивный сценарий создания ACCOUNT - ОР 201
class TestCreateAccount:

    def test_create_account_valid(self):
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

        # Позитивный кейс авторизации USER - ОР 200
        auth_user_request = AuthLoginRequest(username="Max140", password="Pas!sw0rd")

        auth_user_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json=auth_user_request.model_dump(),
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        )
        # Проверка на статус код
        assert auth_user_response.status_code == 200

        auth_login_response = AuthLoginResponse(**auth_user_response.json())
        assert auth_user_request.username == auth_login_response.user.username
        assert auth_login_response.user.role == "ROLE_USER"

        token_user = auth_user_response.json().get("token")

        # Позитивный сценарий создания ACCOUNT - ОР 201
        create_account_response = requests.post(
            url = "http://localhost:4111/api/account/create",
            headers = {
                "accept": "application/json",
                "Authorization": f"Bearer {token_user}"
            }
        )
        assert create_account_response.status_code == 201

        create_account_response = CreateAccountResponse(**create_account_response.json())
        assert create_account_response.balance == 0


    # Негативный сценарий создания ACCOUNT - ОР 403
    def test_create_account_invalid_403(self):
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

        create_account_response = requests.post(
            url = "http://localhost:4111/api/account/create",
            headers = {
                "accept": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
        assert create_account_response.status_code == 403
