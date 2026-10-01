import pytest
from api.classes.api_manager import ApiManager
from api.models.create_user_request import CreateUserRequest
from api.models.credit_repay_request import CreditRepayRequest
from api.models.credit_request_request import CreditRequestRequest
from api.models.deposit_account_request import DepositAccountRequest
from api.models.transfer_account_request import TransferAccountRequest


@pytest.fixture
def create_user_request(api_manager):
    create_user_req =CreateUserRequest(username="Max222", password="Pas!sw0rd", role="ROLE_USER")
    api_manager.admin_steps.create_user(create_user_req)
    return create_user_req

@pytest.fixture
def deposit_account_request_invalid_401(api_manager):
    create_user_req = CreateUserRequest(username="Max22", password="Pas!sw0rd", role="ROLE_USER")
    api_manager.admin_steps.create_user(create_user_req)

    create_account_req = api_manager.user_steps.create_account(create_user_req)

    id_account = create_account_req.id

    deposit_account_req = DepositAccountRequest(accountId=id_account, amount=1000)
    return  deposit_account_req

# --------------------------------------------------------------------------------------------------------------

@pytest.fixture
def deposit_account_request(api_manager):
    create_user_req = CreateUserRequest(username="Max222", password="Pas!sw0rd", role="ROLE_USER")
    api_manager.admin_steps.create_user(create_user_req)

    create_account_req = api_manager.user_steps.create_account(create_user_req)

    id_account = create_account_req.id

    deposit_account_req = DepositAccountRequest(accountId=id_account, amount=1000)
    return create_user_req, create_account_req, deposit_account_req

@pytest.fixture
def deposit_account_request_invalid_400(api_manager):
    create_user_req = CreateUserRequest(username="Max222", password="Pas!sw0rd", role="ROLE_USER")
    api_manager.admin_steps.create_user(create_user_req)

    create_account_req = api_manager.user_steps.create_account(create_user_req)

    id_account = create_account_req.id

    deposit_account_req = DepositAccountRequest(accountId=id_account, amount=-1000)
    return create_user_req, create_account_req, deposit_account_req

# --------------------------------------------------------------------------------------------------------------

@pytest.fixture
def transfer_account_request(api_manager: ApiManager):
    create_user_req = CreateUserRequest(username="Max222", password="Pas!sw0rd", role="ROLE_USER")
    api_manager.admin_steps.create_user(create_user_req)

    create_account_req_one = api_manager.user_steps.create_account(create_user_req)
    id_account_one = create_account_req_one.id

    create_account_req_two = api_manager.user_steps.create_account(create_user_req)
    id_account_two = create_account_req_two.id

    deposit_account_req = DepositAccountRequest(accountId=id_account_one, amount=3000)
    api_manager.user_steps.deposit_account(create_user_req, deposit_account_req)

    transfer_account_req = TransferAccountRequest(fromAccountId=id_account_one, toAccountId=id_account_two, amount=1000)

    return create_user_req, deposit_account_req, transfer_account_req, id_account_one, id_account_two


@pytest.fixture
def transfer_account_request_invalid_401(api_manager: ApiManager):
    create_user_req = CreateUserRequest(username="Max222", password="Pas!sw0rd", role="ROLE_USER")
    api_manager.admin_steps.create_user(create_user_req)

    create_account_req_one = api_manager.user_steps.create_account(create_user_req)
    id_account_one = create_account_req_one.id

    create_account_req_two = api_manager.user_steps.create_account(create_user_req)
    id_account_two = create_account_req_two.id

    deposit_account_req = DepositAccountRequest(accountId=id_account_one, amount=3000)
    api_manager.user_steps.deposit_account(create_user_req, deposit_account_req)

    transfer_account_req = TransferAccountRequest(fromAccountId=id_account_one, toAccountId=id_account_two, amount=1000)

    return deposit_account_req, transfer_account_req, id_account_one, id_account_two

# --------------------------------------------------------------------------------------------------------------

@pytest.fixture
def create_user_request_credit(api_manager):
    create_user_req = CreateUserRequest(username="Max222", password="Pas!sw0rd", role="ROLE_CREDIT_SECRET")
    api_manager.admin_steps.create_user(create_user_req)

    return create_user_req

# --------------------------------------------------------------------------------------------------------------

@pytest.fixture
def credit_repay_request(api_manager: ApiManager):
    create_user_req = CreateUserRequest(username="Max222", password="Pas!sw0rd", role="ROLE_CREDIT_SECRET")
    api_manager.admin_steps.create_user(create_user_req)

    create_account_req = api_manager.user_steps.create_account(create_user_req)

    id_account = create_account_req.id

    credit_request_req = CreditRequestRequest(accountId=id_account, amount=5000, termMonths=12)
    credit = api_manager.user_steps.credit_request(credit_request_req,create_user_req)

    id_credit = credit.creditId

    credit_repay_req = CreditRepayRequest(creditId=id_credit, accountId= id_account, amount=5000)
    return create_user_req, credit_request_req, credit_repay_req, id_credit

@pytest.fixture
def credit_repay_request_invalid_422(api_manager: ApiManager):
    create_user_req = CreateUserRequest(username="Max222", password="Pas!sw0rd", role="ROLE_CREDIT_SECRET")
    api_manager.admin_steps.create_user(create_user_req)

    create_account_req = api_manager.user_steps.create_account(create_user_req)

    id_account = create_account_req.id

    credit_request_req = CreditRequestRequest(accountId=id_account, amount=5000, termMonths=12)
    credit = api_manager.user_steps.credit_request(credit_request_req,create_user_req)

    id_credit = credit.creditId

    credit_repay_req = CreditRepayRequest(creditId=id_credit, accountId= id_account, amount=3000)
    return create_user_req, credit_request_req, credit_repay_req, id_credit