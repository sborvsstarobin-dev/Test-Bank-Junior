import pytest
import requests

@pytest.mark.api
class TestTransferAccount:
    def test_transfer_account_valid(self):
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

        # Позитивный сценарий создания ACCOUNT  №1 - ОР 201
        create_account_response = requests.post(
            url = "http://localhost:4111/api/account/create",
            headers = {
                "accept": "application/json",
                "Authorization": f"Bearer {token_user}"
            }
        )
        assert create_account_response.status_code == 201
        assert create_account_response.json().get("balance") == 0

        id_1 = create_account_response.json().get("id")

        # Позитивный сценарий пополнения счета - ОР 200
        deposit_account_response = requests.post(
            url = "http://localhost:4111/api/account/deposit",
            json = {
                "accountId": id_1,
                "amount": 1000
            },
            headers = {
                "Accept": "application/json",
                "Content-type": "application/json",
                "Authorization": f"Bearer {token_user}"
            }
        )
        assert deposit_account_response.status_code == 200
        assert deposit_account_response.json().get("balance") == 1000
        assert deposit_account_response.json().get("id") == id_1

        # Позитивный сценарий создания ACCOUNT  №2 - ОР 201
        create_account_response = requests.post(
            url = "http://localhost:4111/api/account/create",
            headers = {
                "accept": "application/json",
                "Authorization": f"Bearer {token_user}"
            }
        )
        assert create_account_response.status_code == 201
        assert create_account_response.json().get("balance") == 0

        id_2 = create_account_response.json().get("id")

        # Позитивный сценарий перевода - ОР 200
        transfer_account_response = requests.post(
            url = "http://localhost:4111/api/account/transfer",
            json = {
                "fromAccountId": id_1,
                "toAccountId": id_2,
                "amount": 600
            },
            headers = {
                "accept": "application/json",
                "Content-type": "application/json",
                "Authorization": f"Bearer {token_user}"
            }
        )

        assert transfer_account_response.status_code == 200
        assert transfer_account_response.json().get("fromAccountId") == id_1
        assert transfer_account_response.json().get("toAccountId") == id_2
        assert transfer_account_response.json().get("fromAccountIdBalance") == 400


    def test_transfer_account_invalid_401(self):
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

        # Позитивный сценарий создания ACCOUNT  №1 - ОР 201
        create_account_response = requests.post(
            url = "http://localhost:4111/api/account/create",
            headers = {
                "accept": "application/json",
                "Authorization": f"Bearer {token_user}"
            }
        )
        assert create_account_response.status_code == 201
        assert create_account_response.json().get("balance") == 0

        id_1 = create_account_response.json().get("id")

        # Позитивный сценарий пополнения счета - ОР 200
        deposit_account_response = requests.post(
            url = "http://localhost:4111/api/account/deposit",
            json = {
                "accountId": id_1,
                "amount": 1000
            },
            headers = {
                "Accept": "application/json",
                "Content-type": "application/json",
                "Authorization": f"Bearer {token_user}"
            }
        )
        assert deposit_account_response.status_code == 200
        assert deposit_account_response.json().get("balance") == 1000
        assert deposit_account_response.json().get("id") == id_1

        # Позитивный сценарий создания ACCOUNT  №2 - ОР 201
        create_account_response = requests.post(
            url = "http://localhost:4111/api/account/create",
            headers = {
                "accept": "application/json",
                "Authorization": f"Bearer {token_user}"
            }
        )
        assert create_account_response.status_code == 201
        assert create_account_response.json().get("balance") == 0

        id_2 = create_account_response.json().get("id")

        # Негативный сценарий сценарий перевода - ОР 401
        transfer_account_response = requests.post(
            url = "http://localhost:4111/api/account/transfer",
            json = {
                "fromAccountId": id_1,
                "toAccountId": id_2,
                "amount": 600
            },
            headers = {
                "accept": "application/json",
                "Content-type": "application/json",
                "Authorization": f"Bearer "
            }
        )

        assert transfer_account_response.status_code == 401







