from api.foundation.endpoint import Endpoint
from api.foundation.requesters.crud_requester import CrudRequester
from api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from api.models import credit_request_request
from api.models.create_user_request import CreateUserRequest
from api.models.credit_repay_request import CreditRepayRequest
from api.models.credit_request_request import CreditRequestRequest
from api.models.deposit_account_request import DepositAccountRequest
from api.models.transfer_account_request import TransferAccountRequest
from api.specs.request_specs import RequestSpecs
from api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class UserSteps(BaseSteps):
    def create_account(self, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.status_code_201()
        ).post()
        return response


    def create_account_invalide_403(self):
        CrudRequester(
            RequestSpecs.auth_headers(username="admin", password="123456"),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.status_code_403()
        ).post()

#--------------------------------------------------------------------------------------------------------------

    def deposit_account(self, create_user_request: CreateUserRequest, deposit_account_request: DepositAccountRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.DEPOSIT_ACCOUNT,
            ResponseSpecs.status_code_200()
        ).post(deposit_account_request)
        return response


    def deposit_account_invalid_400(self, create_user_request: CreateUserRequest, deposit_account_request: DepositAccountRequest):
        CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.DEPOSIT_ACCOUNT,
            ResponseSpecs.status_code_400()
        ).post(deposit_account_request)


    def deposit_account_invalid_401(self, deposit_account_request: DepositAccountRequest):
        CrudRequester(
            RequestSpecs.no_auth_headers(),
            Endpoint.DEPOSIT_ACCOUNT,
            ResponseSpecs.status_code_401()
        ).post(deposit_account_request)

    # --------------------------------------------------------------------------------------------------------------

    def transfer_account(self, create_user_request: CreateUserRequest,transfer_account_request: TransferAccountRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.TRANSFER_ACCOUNT,
            ResponseSpecs.status_code_200()
        ).post(transfer_account_request)
        return response

    def transfer_account_invalid_401(self, transfer_account_request: TransferAccountRequest):
        CrudRequester(
            RequestSpecs.no_auth_headers(),
            Endpoint.TRANSFER_ACCOUNT,
            ResponseSpecs.status_code_401()
        ).post(transfer_account_request)

# --------------------------------------------------------------------------------------------------------------

    def credit_request(self, credit_request_request: CreditRequestRequest, create_user_request_credit):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request_credit.username, password=create_user_request_credit.password),
            Endpoint.CREDIT_REQUEST,
            ResponseSpecs.status_code_201()
        ).post(credit_request_request)
        return response

    def credit_request_invalid_404(self, credit_request_request: CreditRequestRequest, create_user_request_credit):
        CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request_credit.username, password=create_user_request_credit.password),
            Endpoint.CREDIT_REQUEST,
            ResponseSpecs.status_code_404()
        ).post(credit_request_request)

# --------------------------------------------------------------------------------------------------------------

    def credit_repay(self, credit_repay_request: CreditRepayRequest, create_user_request_credit):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request_credit.username, password=create_user_request_credit.password),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.status_code_200()
        ).post(credit_repay_request)
        return response

    def credit_repay_invalid_422(self, credit_repay_request: CreditRepayRequest, create_user_request_credit):
        CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request_credit.username, password=create_user_request_credit.password),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.status_code_422()
        ).post(credit_repay_request)