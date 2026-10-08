import pytest
from src.main.api.fixtures.db_fixture import db_session
from sqlalchemy.orm import Session
from api.classes.api_manager import ApiManager
from api.models.create_user_request import CreateUserRequest
from src.main.api.db.crud.account_crud import AccountCrudDb as Account


@pytest.mark.api
class TestDepositAccount:
    # Позитивный сценарий пополнения счёта - ОР 200
    def test_deposit_account_valid(self, api_manager: ApiManager, deposit_account_request, db_session: Session):
        create_user_req, create_account_req, deposit_account_req = deposit_account_request
        response = api_manager.user_steps.deposit_account(create_user_req, deposit_account_req)

        assert response.balance == deposit_account_req.amount

        account_from_db = Account.get_account_by_id(db_session, deposit_account_req.accountId)
        assert account_from_db.balance == deposit_account_req.amount, "Баланс в БД не совпадает с суммой пополнения "

    # Негативный сценарий пополнения счёта - ОР 400 (Некорректное тело запроса)
    def test_deposit_account_invalid_400(self, api_manager: ApiManager, deposit_account_request_invalid_400,
                                         db_session: Session):
        create_user_req, create_account_req, deposit_account_req = deposit_account_request_invalid_400
        api_manager.user_steps.deposit_account_invalid_400(create_user_req, deposit_account_req)

        account_from_db = Account.get_account_by_id(db_session, deposit_account_req.accountId)
        assert account_from_db is not None, "Счет должен существовать"
        assert account_from_db.balance == 0, "Баланс не должен измениться при ошибке 400"

    # Негативный сценарий пополнения счёта - ОР 401 (Пользователь не авторизован)
    def test_deposit_account_invalid_401(self, api_manager: ApiManager, create_user_request: CreateUserRequest,
                                         deposit_account_request_invalid_401, db_session: Session):
        deposit_account_req = deposit_account_request_invalid_401
        api_manager.user_steps.deposit_account_invalid_401(deposit_account_req)

        account_from_db = Account.get_account_by_id(db_session, deposit_account_req.accountId)
        assert account_from_db is not None, "Счет должен существовать"
        assert account_from_db.balance == 0, "Баланс не должен измениться при ошибке 401"
