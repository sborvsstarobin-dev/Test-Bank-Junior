import pytest


@pytest.mark.api

class TestCreateAccount:
    # Позитивный сценарий создания ACCOUNT - ОР 201
    def test_create_account_valid(self, api_manager, create_user_request):
        response = api_manager.user_steps.create_account(create_user_request)

        assert response.balance == 0




    # Негативный сценарий создания ACCOUNT - ОР 403 (Создание под Админом)
    def test_create_account_invalid_403(self, api_manager):
       api_manager.user_steps.create_account_invalide_403()

