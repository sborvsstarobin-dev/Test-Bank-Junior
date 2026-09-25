import pytest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api

class TestCreateUser:
    # Позитивный сценарий создания User - ОР 200
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

        # Негативный сценарий создания User - ОР 400
        create_user_request = CreateUserRequest(username=username, password=password, role="ROLE_USER")

        CreateUserRequester(
            request_spec=RequestSpecs.auth_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.status_code_400(),
        ).post(create_user_request)




# Негативный сценарий создания User - ОР 401
    def test_create_user_invalid_401(self):
        # Позитивный кейс авторизации ADMIN - ОР 200

        # Негативный сценарий создания User - ОР 401
        create_user_request = CreateUserRequest(username = "Max10", password = "Pas!sw0rd", role = "ROLE_USER")

        CreateUserRequester(
            request_spec=RequestSpecs.no_auth_headers(),
            response_spec=ResponseSpecs.status_code_401(),
        ).post(create_user_request)