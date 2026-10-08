import pytest
from api.classes.api_manager import ApiManager
from api.models.transfer_account_request import TransferAccountRequest
from src.main.api.fixtures.db_fixture import db_session
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from sqlalchemy.orm import Session
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction


@pytest.mark.api
class TestTransferAccount:
    # Позитивный сценарий перевода счёта - ОР 200
    def test_transfer_account_valid_one_user(self, api_manager: ApiManager,
                                             transfer_account_request: TransferAccountRequest, db_session: Session):
        create_user_req, deposit_account_req, transfer_account_req, id_account_one, id_account_two = transfer_account_request
        response = api_manager.user_steps.transfer_account(create_user_req, transfer_account_req)

        assert response.fromAccountId == transfer_account_req.fromAccountId
        assert response.toAccountId == transfer_account_req.toAccountId
        expected_balance = deposit_account_req.amount - transfer_account_req.amount
        assert response.fromAccountIdBalance == expected_balance

        account_from_db = Account.get_account_by_id(db_session, id_account_one)
        assert account_from_db.balance == expected_balance

        transaction_from_db_one = Transaction.get_transaction_by_from_account_id(db_session, id_account_one)
        assert transaction_from_db_one.from_account_id == transfer_account_req.fromAccountId

        transaction_from_db_two = Transaction.get_transaction_by_to_account_id(db_session, id_account_two)
        assert transaction_from_db_two.to_account_id == transfer_account_req.toAccountId

    # Негативный сценарий перевода счёта - ОР 401(Пользователь не авторизован)
    def test_transfer_account_invalid_401(self, api_manager: ApiManager, transfer_account_request_invalid_401,
                                          db_session: Session):
        deposit_account_req, transfer_account_req, id_account_one, id_account_two = transfer_account_request_invalid_401
        api_manager.user_steps.transfer_account_invalid_401(transfer_account_req)

        account_from_db = Account.get_account_by_id(db_session, id_account_two)
        assert account_from_db.balance == 0

        transaction_from_db_one = Transaction.get_transaction_by_from_account_id(db_session, id_account_two)
        assert transaction_from_db_one is None
