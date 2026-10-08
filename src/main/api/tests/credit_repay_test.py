import pytest
from api.classes.api_manager import ApiManager
from sqlalchemy.orm import Session
from api.fixtures.db_fixture import db_session
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit


@pytest.mark.api
class TestCreditRepay:
    # Позитивный сценарий погашения кредита - ОР 200
    def test_credit_repay_valid(self, api_manager: ApiManager, credit_repay_request, db_session: Session):
        create_user_req, credit_request_req, credit_repay_req, id_credit = credit_repay_request

        response = api_manager.user_steps.credit_repay(credit_repay_req, create_user_req)

        assert credit_repay_req.creditId == id_credit
        assert response.amountDeposited == credit_repay_req.amount

        credit_from_db = Credit.get_credit_by_account_id(db_session, credit_request_req.accountId)
        assert credit_from_db.account_id == credit_repay_req.accountId
        assert credit_from_db.amount == credit_repay_req.amount
        assert credit_from_db.term_months == credit_request_req.termMonths
        assert credit_from_db.balance == 0

    # Негативный сценарий погашения кредита - ОР 422 (Суммы недостаточно)
    def test_credit_repay_invalid_422(self, api_manager: ApiManager, credit_repay_request_invalid_422,
                                      db_session: Session):
        create_user_req, credit_request_req, credit_repay_req, id_credit = credit_repay_request_invalid_422

        api_manager.user_steps.credit_repay_invalid_422(credit_repay_req, create_user_req)

        credit_from_db = Credit.get_credit_by_account_id(db_session, credit_request_req.accountId)
        assert credit_from_db.account_id == credit_request_req.accountId
        assert credit_from_db.amount == credit_request_req.amount
        assert credit_from_db.term_months == credit_request_req.termMonths
        assert credit_from_db.balance == -credit_request_req.amount
