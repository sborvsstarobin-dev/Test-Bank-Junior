import requests
import pytest

from src.main.api.models.auth_login_request import AuthLoginRequest
from src.main.api.models.auth_login_response import AuthLoginResponse

@pytest.mark.api
# Позитивный кейс авторизации ADMIN - ОР 200
class TestAuthAdmin:

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

        # Проверка на имя и роль
        auth_login_response = AuthLoginResponse(**auth_admin_response.json())
        assert auth_admin_request.username == auth_login_response.user.username
        assert auth_login_response.user.role == "ROLE_ADMIN"


    @pytest.mark.parametrize(
        "username,password",
        [
            ("", "123456"),  # Отсутствует логин - ОР 400
            ("admin", "")    # Отсутствует пароль - ОР 400
        ]
    )

    # Негативный кейс авторизации ADMIN - ОР 400
    def test_auth_login_invalid_username(self, username, password):
        auth_admin_request = AuthLoginRequest(username = username, password = password)

        auth_admin_response = requests.post(
            url = "http://localhost:4111/api/auth/token/login",
            json = auth_admin_request.model_dump(),
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        )
        # Проверка на статус код
        assert auth_admin_response.status_code == 400

    @pytest.mark.parametrize(
        "username,password",
        [
            ("kldndf", "123456"),  # Неправильный логин - ОР 401
            ("admin", "dsfsf33")  # Неправильный пароль - ОР 401
        ]
    )
    # Негативный кейс авторизации ADMIN - ОР 401
    def test_auth_login_invalid_username(self, username, password):
        auth_admin_request = AuthLoginRequest(username = username, password = password)

        auth_admin_response = requests.post(
            url = "http://localhost:4111/api/auth/token/login",
            json = auth_admin_request.model_dump(),
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        )
        # Проверка на статус код
        assert auth_admin_response.status_code == 401