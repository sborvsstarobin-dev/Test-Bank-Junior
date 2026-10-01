from dataclasses import dataclass
from enum import Enum
from typing import Optional, Type
from api.models.auth_login_request import AuthLoginRequest
from api.models.auth_login_response import AuthLoginResponse
from api.models.create_account_response import CreateAccountResponse
from api.models.credit_repay_request import CreditRepayRequest
from api.models.credit_repay_response import CreditRepayResponse
from api.models.credit_request_request import CreditRequestRequest
from api.models.credit_request_response import CreditRequestResponse
from api.models.deposit_account_request import DepositAccountRequest
from api.models.deposit_account_response import DepositAccountResponse
from api.models.transfer_account_request import TransferAccountRequest
from api.models.transfer_account_response import TransferAccountResponse
from api.specs import response_specs
from src.main.api.models.base_model import BaseModel
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse


@dataclass
class EndpointConfiguration:
    url: str
    request_model: Optional[Type[BaseModel]]
    response_model: Optional[Type[BaseModel]]


class Endpoint(Enum):
    #DEPOSIT_ACCOUNT = None
    ADMIN_CREAT_USER =EndpointConfiguration(
        url="/admin/create",
        request_model=CreateUserRequest,
        response_model=CreateUserResponse
    )


    USER_LOGIN = EndpointConfiguration(
        url="/auth/token/login",
        request_model= AuthLoginRequest,
        response_model= AuthLoginResponse
    )

    CREATE_ACCOUNT = EndpointConfiguration(
        url="/account/create",
        request_model= None,
        response_model= CreateAccountResponse
    )


    ADMIN_DELETE_USER = EndpointConfiguration(
        url="/admin/users",
        request_model= None,
        response_model= None
    )

    DEPOSIT_ACCOUNT = EndpointConfiguration(
        url="/account/deposit",
        request_model= DepositAccountRequest,
        response_model= DepositAccountResponse
    )

    TRANSFER_ACCOUNT = EndpointConfiguration(
        url="/account/transfer",
        request_model= TransferAccountRequest,
        response_model= TransferAccountResponse
    )

    CREDIT_REQUEST = EndpointConfiguration(
        url="/credit/request",
        request_model= CreditRequestRequest,
        response_model = CreditRequestResponse
    )

    CREDIT_REPAY = EndpointConfiguration(
        url="/credit/repay",
        request_model= CreditRepayRequest,
        response_model = CreditRepayResponse
    )