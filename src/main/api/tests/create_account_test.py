import pytest
from sqlalchemy.orm import Session
from api.classes.api_manager import ApiManager
from api.models.create_user_request import CreateUserRequest
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.fixtures.db_fixture import db_session


@pytest.mark.api
class TestCreateAccount:
    # Позитивный сценарий создания ACCOUNT - ОР 201
    def test_create_account_valid(self, api_manager: ApiManager, create_user_request: CreateUserRequest,
                                  db_session: Session):
        response = api_manager.user_steps.create_account(create_user_request)

        assert response.balance == 0

        account_from_db = Account.get_account_by_id(db_session, response.id)
        assert account_from_db.id == response.id, "Аккаунт не создан, ID нет в БД"
        assert account_from_db.balance is not None, "Поле balance отсутствует в БД"

    # Негативный сценарий создания ACCOUNT - ОР 403 (Создание под Админом)
    def test_create_account_invalid_403(self, api_manager: ApiManager, db_session: Session):
        before_count = Account.count_all(db_session)
        api_manager.user_steps.create_account_invalide_403()

        after_count = Account.count_all(db_session)
        assert before_count == after_count, "Аккаунт создан = ошибка"


