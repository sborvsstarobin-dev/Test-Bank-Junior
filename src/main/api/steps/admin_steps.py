from api.models.auth_login_request import AuthLoginRequest
from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps



class AdminSteps(BaseSteps):
    def create_user(self, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username="admin", password="123456"),
            Endpoint.ADMIN_CREAT_USER,
            ResponseSpecs.status_code_200(),
        ).post(create_user_request)

        self.created_obj.append(response)
        return response


    def create_user_invalid_400(self, create_user_request: CreateUserRequest):
        CrudRequester(
            RequestSpecs.auth_headers(username="admin", password="123456"),
            Endpoint.ADMIN_CREAT_USER,
            ResponseSpecs.status_code_400(),
        ).post(create_user_request)


    def create_user_invalid_401(self, create_user_request: CreateUserRequest):
        CrudRequester(
            RequestSpecs.no_auth_headers(),
            Endpoint.ADMIN_CREAT_USER,
            ResponseSpecs.status_code_401(),
        ).post(create_user_request)
#_____________________________________________________________________________________________
#_____________________________________________________________________________________________

    def login_user(self, auth_login_request: AuthLoginRequest):
        response = ValidateCrudRequester(
            RequestSpecs.no_auth_headers(),
            Endpoint.USER_LOGIN,
            ResponseSpecs.status_code_200()
        ).post(auth_login_request)
        return response

    def login_user_invalid_400(self, auth_login_request: AuthLoginRequest):
        CrudRequester(
            RequestSpecs.no_auth_headers(),
            Endpoint.USER_LOGIN,
            ResponseSpecs.status_code_400()
        ).post(auth_login_request)

    def login_user_invalid_401(self, auth_login_request: AuthLoginRequest):
        CrudRequester(
            RequestSpecs.no_auth_headers(),
            Endpoint.USER_LOGIN,
            ResponseSpecs.status_code_401()
        ).post(auth_login_request)


    def delete_user(self,user_id: int):
        CrudRequester(
            RequestSpecs.auth_headers(username="admin", password="123456"),
            Endpoint.ADMIN_DELETE_USER,
            ResponseSpecs.status_code_200(),
        ).delete(user_id)


