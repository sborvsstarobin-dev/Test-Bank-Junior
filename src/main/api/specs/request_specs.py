import requests

from src.main.api.models.auth_login_request import AuthLoginRequest
from src.main.api.models.auth_login_response import AuthLoginResponse

class RequestSpecs:
    BASE_URL = 'http://localhost:4111/api'
    @staticmethod
    def base_headers():
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    @staticmethod
    def auth_headers(username: str, password: str):
        request = AuthLoginRequest(username=username, password=password)
        responce = requests.post(
            url='http://localhost:4111/api/auth/token/login',
            json=request.model_dump(),
            headers= RequestSpecs.base_headers()
        )

        if responce.status_code == 200:
            responce_data = AuthLoginResponse(**responce.json())
            token = responce_data.token

            headers = RequestSpecs.base_headers()
            headers['Authorization'] = f'Bearer {token}'

            return {
                'headers': headers,
                "base_url": RequestSpecs.BASE_URL,
            }

        raise Exception("Failed to authorization")
