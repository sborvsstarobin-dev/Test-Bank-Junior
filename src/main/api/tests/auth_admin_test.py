import pytest
from api.fixtures.api_fixture import api_manager
from src.main.api.models.auth_login_request import AuthLoginRequest


@pytest.mark.api

class TestAuthAdmin:
    # Позитивный кейс авторизации ADMIN - ОР 200
    def test_auth_admin_valid(self, api_manager):

        auth_admin_request = AuthLoginRequest(username = "admin", password = "123456")

        response = api_manager.admin_steps.login_user(auth_admin_request)

        assert response.user.username == auth_admin_request.username
        assert response.user.role == "ROLE_ADMIN"


    @pytest.mark.parametrize(
        "username,password",
        [
            ("", "123456"),  # Отсутствует логин - ОР 400
            ("admin", "")    # Отсутствует пароль - ОР 400
        ]
    )
    # Негативный кейс авторизации ADMIN - ОР 400
    def test_auth_admin_invalid_400(self, username, password, api_manager):
        auth_admin_request = AuthLoginRequest(username = username, password = password)

        response = api_manager.admin_steps.login_user_invalid_400(auth_admin_request)



    @pytest.mark.parametrize(
        "username,password",
        [
            ("kldndf", "123456"),  # Неправильный логин - ОР 401
            ("admin", "dsfsf33")  # Неправильный пароль - ОР 401
        ]
    )
    # Негативный кейс авторизации ADMIN - ОР 401
    def test_auth_admin_invalid_401(self, username, password, api_manager):
        auth_admin_request = AuthLoginRequest(username = username, password = password)

        response = api_manager.admin_steps.login_user_invalid_401(auth_admin_request)





    # Позитивный кейс авторизации USER - ОР 200
    def test_auth_user_valid(self, api_manager, create_user_request):
        response = api_manager.admin_steps.login_user(create_user_request)

        assert response.user.username == create_user_request.username
        assert response.user.role == create_user_request.role


    # Негативный кейс авторизации USER - ОР 401 (Некорректный пароль)
    def test_auth_user_invalid_401(self, api_manager, create_user_request):
        auth_admin_request = AuthLoginRequest(username = "Max222", password = "Pas!sw0r")
        api_manager.admin_steps.login_user_invalid_401(auth_admin_request)
