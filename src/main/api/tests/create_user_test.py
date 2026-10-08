import pytest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.models.user_table import User
from src.main.api.fixtures.api_fixture import api_manager
from src.main.api.models.create_user_request import CreateUserRequest
from sqlalchemy.orm import Session
from src.main.api.db.crud.user_crud import UserCrudDb as User

@pytest.mark.api

class TestCreateUser:
    # Позитивный сценарий создания User - ОР 200
    def test_create_user_valid(self, api_manager: ApiManager, db_session: Session):
        # Позитивный кейс авторизации ADMIN - ОР 200

        # Позитивный сценарий создания User - ОР 200
        create_user_request = CreateUserRequest(username = "Max170", password = "Pas!sw0rd", role = "ROLE_USER")

        response = api_manager.admin_steps.create_user(create_user_request)

        assert create_user_request.username == response.username
        assert create_user_request.role == response.role

        user_from_db = User.get_user_by_username(db_session, create_user_request.username)
        assert user_from_db.username == create_user_request.username



    @pytest.mark.parametrize(
        "username,password",
        [ ("Саша", "Pas!sw0rd"), # Негативный сценарий, кириллица в логине - ОР 400
          ("ad", "Pas!sw0rd"),  # Негативный сценарий, меньше 3 символов в логине - ОР 400
          ("adminadminadminadmin", "Pas!sw0rd"),  # Негативный сценарий, больше 15 символов в логине - ОР 400
          ("admin!", "Pas!sw0rd"),  # Негативный сценарий, спецсимволы в логине - ОР 400
          ("Max2000", "фPas!sфw0rd"),  # Негативный сценарий, кириллица в пароле - ОР 400
          ("Max2000", "Pas!sw0"),  # Негативный сценарий, меньше 8 символов в пароле - ОР 400
          ("Max2000", "pas!sw0rd"),  # Негативный сценарий, без заглавных букв в пароле - ОР 400
          ("Max2000", "PAS!SWORD"),  # Негативный сценарий, без маленьких букв в пароле - ОР 400
          ("Max2000", "Passsw0rd"),  # Негативный сценарий, без спецсимволов в пароле - ОР 400
          ("Max2000", "Pas!sword")  # Негативный сценарий, без цифр в пароле - ОР 400
        ]
    )


    # Негативный сценарий создания User - ОР 400
    def test_create_user_invalid_400(self, db_session: Session, username, password, api_manager: ApiManager):
        # Позитивный кейс авторизации ADMIN - ОР 200

        # Негативный сценарий создания User - ОР 400
        create_user_request = CreateUserRequest(username=username, password=password, role="ROLE_USER")
        api_manager.admin_steps.create_user_invalid_400(create_user_request)

        user_from_db = User.get_user_by_username(db_session, create_user_request.username)
        assert user_from_db is None, "Пользователь создан - ошибка"



# Негативный сценарий создания User - ОР 401
    def test_create_user_invalid_401(self, db_session: Session, api_manager: ApiManager):
        # Позитивный кейс авторизации ADMIN - ОР 200

        # Негативный сценарий создания User - ОР 401
        create_user_request = CreateUserRequest(username = "Max10", password = "Pas!sw0rd", role = "ROLE_USER")
        api_manager.admin_steps.create_user_invalid_401(create_user_request)

        user_from_db = User.get_user_by_username(db_session, create_user_request.username)
        assert user_from_db is None, "Пользователь создан - ошибка"