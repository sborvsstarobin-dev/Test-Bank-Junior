from http import HTTPStatus
import requests
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.requests.requester import Requester
from requests import Response

class CreateAccountRequester(Requester):
    def post(self,model = None)->CreateAccountResponse | Response:
        url = f"{self.base_url}/account/create"
        response = requests.post(
            url =url,
            headers=self.headers,
        )
        self.response_spec(response)

        if response.status_code == HTTPStatus.CREATED:
            return CreateAccountResponse(**response.json())
        return response
