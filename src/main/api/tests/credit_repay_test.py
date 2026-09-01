import pytest
import requests

@pytest.mark.api
class TestCreditRepay:
    def test_credit_repay_valid(self):
        # Позитивный кейс авторизации ADMIN - ОР 200
        auth_admin_response = requests.post(
            url = "http://localhost:4111/api/auth/token/login",
            json = {
                "username": "admin",
                "password": "123456"
            },
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        )
        # Проверка на статус код
        assert auth_admin_response.status_code == 200
        assert auth_admin_response.json()["user"]["username"] == "admin"
        assert auth_admin_response.json()["user"]["role"] == "ROLE_ADMIN"

        token = auth_admin_response.json().get("token")


        # Позитивный сценарий создания USER - ОР 200
        create_user_response = requests.post(
            url = "http://localhost:4111/api/admin/create",
            json = {
                "username": "Max1400",
                "password": "Pas!sw0rd",
                "role": "ROLE_CREDIT_SECRET"
            },
            headers = {
                "Content-Type": "application/json",
                "Accept": "*/*",
                "Authorization": f"Bearer {token}"
            }
        )
        assert create_user_response.status_code == 200
        assert create_user_response.json().get("username") == "Max1400"
        assert create_user_response.json().get("role") == "ROLE_CREDIT_SECRET"

        # Позитивный кейс авторизации USER - ОР 200
        auth_user_response = requests.post(
            url = "http://localhost:4111/api/auth/token/login",
            json = {
                "username": "Max1400",
                "password": "Pas!sw0rd"
            },
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        )
        # Проверка на статус код
        assert auth_user_response.status_code == 200
        assert auth_user_response.json()["user"]["username"] == "Max1400"
        assert auth_user_response.json()["user"]["role"] == "ROLE_CREDIT_SECRET"

        token_user = auth_user_response.json().get("token")

        # Позитивный сценарий создания ACCOUNT - ОР 201
        create_account_response = requests.post(
            url = "http://localhost:4111/api/account/create",
            headers = {
                "accept": "application/json",
                "Authorization": f"Bearer {token_user}"
            }
        )
        assert create_account_response.status_code == 201
        assert create_account_response.json().get("balance") == 0

        id_account = create_account_response.json().get("id")

        # Позитивный сценарий получения кредита - ОР 201
        credit_request_response = requests.post(
            url = "http://localhost:4111/api/credit/request",
            json = {
                "accountId": id_account,
                "amount": 5000,
                "termMonths": 12
            },
            headers = {
                "Accept": "application/json",
                "Content-type": "application/json",
                "Authorization": f"Bearer {token_user}"
            }
        )
        assert credit_request_response.status_code == 201
        assert credit_request_response.json().get("amount") == 5000
        assert credit_request_response.json().get("termMonths") == 12

        id_credit = credit_request_response.json().get("creditId")

        # Позитивный сценарий погашения кредита - ОР 200
        credit_repay_response = requests.post(
            url = "http://localhost:4111/api/credit/repay",
            json = {
                "creditId": id_credit,
                "accountId": id_account,
                "amount": 5000
            },
            headers = {
                "Accept": "application/json",
                "Content-type": "application/json",
                "Authorization": f"Bearer {token_user}"
            }
        )
        assert credit_repay_response.status_code == 200
        assert credit_repay_response.json().get("amountDeposited") == 5000


    def test_credit_repay_invalid_422(self):
        # Позитивный кейс авторизации ADMIN - ОР 200
        auth_admin_response = requests.post(
            url = "http://localhost:4111/api/auth/token/login",
            json = {
                "username": "admin",
                "password": "123456"
            },
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        )
        # Проверка на статус код
        assert auth_admin_response.status_code == 200
        assert auth_admin_response.json()["user"]["username"] == "admin"
        assert auth_admin_response.json()["user"]["role"] == "ROLE_ADMIN"

        token = auth_admin_response.json().get("token")


        # Позитивный сценарий создания USER - ОР 200
        create_user_response = requests.post(
            url = "http://localhost:4111/api/admin/create",
            json = {
                "username": "Max1400",
                "password": "Pas!sw0rd",
                "role": "ROLE_CREDIT_SECRET"
            },
            headers = {
                "Content-Type": "application/json",
                "Accept": "*/*",
                "Authorization": f"Bearer {token}"
            }
        )
        assert create_user_response.status_code == 200
        assert create_user_response.json().get("username") == "Max1400"
        assert create_user_response.json().get("role") == "ROLE_CREDIT_SECRET"

        # Позитивный кейс авторизации USER - ОР 200
        auth_user_response = requests.post(
            url = "http://localhost:4111/api/auth/token/login",
            json = {
                "username": "Max1400",
                "password": "Pas!sw0rd"
            },
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        )
        # Проверка на статус код
        assert auth_user_response.status_code == 200
        assert auth_user_response.json()["user"]["username"] == "Max1400"
        assert auth_user_response.json()["user"]["role"] == "ROLE_CREDIT_SECRET"

        token_user = auth_user_response.json().get("token")

        # Позитивный сценарий создания ACCOUNT - ОР 201
        create_account_response = requests.post(
            url = "http://localhost:4111/api/account/create",
            headers = {
                "accept": "application/json",
                "Authorization": f"Bearer {token_user}"
            }
        )
        assert create_account_response.status_code == 201
        assert create_account_response.json().get("balance") == 0

        id_account = create_account_response.json().get("id")

        # Позитивный сценарий получения кредита - ОР 201
        credit_request_response = requests.post(
            url = "http://localhost:4111/api/credit/request",
            json = {
                "accountId": id_account,
                "amount": 5000,
                "termMonths": 12
            },
            headers = {
                "Accept": "application/json",
                "Content-type": "application/json",
                "Authorization": f"Bearer {token_user}"
            }
        )
        assert credit_request_response.status_code == 201
        assert credit_request_response.json().get("amount") == 5000
        assert credit_request_response.json().get("termMonths") == 12

        id_credit = credit_request_response.json().get("creditId")

        # Негативный сценарий погашения кредита - ОР 422
        credit_repay_response = requests.post(
            url = "http://localhost:4111/api/credit/repay",
            json = {
                "creditId": id_credit,
                "accountId": id_account,
                "amount": 3000
            },
            headers = {
                "Accept": "application/json",
                "Content-type": "application/json",
                "Authorization": f"Bearer {token_user}"
            }
        )
        assert credit_repay_response.status_code == 422
        assert credit_repay_response.json().get("error") == "The amount is not enough. Credit balance: -5000"

