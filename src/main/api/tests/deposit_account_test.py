import pytest
import requests

@pytest.mark.api
class TestDepositAccount:
    def test_deposit_account_valid(self):
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
                "role": "ROLE_USER"
            },
            headers = {
                "Content-Type": "application/json",
                "Accept": "*/*",
                "Authorization": f"Bearer {token}"
            }
        )
        assert create_user_response.status_code == 200
        assert create_user_response.json().get("username") == "Max1400"
        assert create_user_response.json().get("role") == "ROLE_USER"

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
        assert auth_user_response.json()["user"]["role"] == "ROLE_USER"

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

        # Позитивный сценарий пополнения счета - ОР 200
        deposit_account_response = requests.post(
            url = "http://localhost:4111/api/account/deposit",
            json = {
                "accountId": id_account,
                "amount": 1000.5
            },
            headers = {
                "Accept": "application/json",
                "Content-type": "application/json",
                "Authorization": f"Bearer {token_user}"
            }
        )
        assert deposit_account_response.status_code == 200
        assert deposit_account_response.json().get("balance") == 1000.5
        assert deposit_account_response.json().get("id") == id_account

    def test_deposit_account_invalid_400(self):
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
                "role": "ROLE_USER"
            },
            headers = {
                "Content-Type": "application/json",
                "Accept": "*/*",
                "Authorization": f"Bearer {token}"
            }
        )
        assert create_user_response.status_code == 200
        assert create_user_response.json().get("username") == "Max1400"
        assert create_user_response.json().get("role") == "ROLE_USER"

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
        assert auth_user_response.json()["user"]["role"] == "ROLE_USER"

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

        # Негативный сценарий пополнения счета - ОР 400
        deposit_account_response = requests.post(
            url = "http://localhost:4111/api/account/deposit",
            json = {
                "accountId": id_account,
                "amount": "1000.5"
            },
            headers = {
                "Accept": "application/json",
                "Content-type": "application/json",
                "Authorization": f"Bearer {token_user}"
            }
        )
        assert deposit_account_response.status_code == 400

    def test_deposit_account_invalid_401(self):
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
                "role": "ROLE_USER"
            },
            headers = {
                "Content-Type": "application/json",
                "Accept": "*/*",
                "Authorization": f"Bearer {token}"
            }
        )
        assert create_user_response.status_code == 200
        assert create_user_response.json().get("username") == "Max1400"
        assert create_user_response.json().get("role") == "ROLE_USER"

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
        assert auth_user_response.json()["user"]["role"] == "ROLE_USER"

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

        # Негативный сценарий пополнения счета - ОР 401
        deposit_account_response = requests.post(
            url = "http://localhost:4111/api/account/deposit",
            json = {
                "accountId": id_account,
                "amount": 1000.5
            },
            headers = {
                "Accept": "application/json",
                "Content-type": "application/json",
                "Authorization": f"Bearer "
            }
        )
        assert deposit_account_response.status_code == 401


