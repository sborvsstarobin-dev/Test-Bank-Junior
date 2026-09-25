from http import HTTPStatus
import requests
from src.main.api.models.auth_login_request import AuthLoginRequest
from src.main.api.models.auth_login_response import AuthLoginResponse
from requests import Response
from src.main.api.requests.requester import Requester

class LoginUserRequester(Requester):
    def post(self, auth_login_request: AuthLoginRequest)-> AuthLoginResponse | Response:
        url = f"{self.base_url}/auth/token/login"

        response = requests.post(
            url = url,
            json = auth_login_request.model_dump(),
            headers = self.headers
        )
        self.response_spec(response)

        if response.status_code == HTTPStatus.OK:
            return AuthLoginResponse(**response.json())
        return response