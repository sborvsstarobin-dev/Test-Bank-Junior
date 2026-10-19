import allure
from src.main.ui.pages.login_page import LoginPage
from playwright.sync_api import Page, expect
from src.main.ui.pages.catalog_page import CatalogPage


class CatalogSteps:
    def __init__(self, page: Page):
        self.page = page
        self.catalog_page = CatalogPage(self.page)

    @allure.step("Открываем страницу каталога")
    def open_catalog_page(self):
        self.catalog_page.open()
        return self

    @allure.step("Выполняем логаут, проверяем корректность редиректа")
    def logout(self):
        self.catalog_page.logout()
        expect(self.page).to_have_url(LoginPage.URL)
        expect(self.page.locator("#login-button")).to_be_visible()
        return self

    @allure.step("Сортируем товары по вписанному фильтру {option}")
    def sort_items(self, option: str):
        self.catalog_page.sort_catalog_items(option)
        return self

    @allure.step("Переход на страницу корзины")
    def open_cart(self):
        self.catalog_page.open_cart()
        return self

    @allure.step("Добавляем товар {product_name} в корзины")
    def add_to_cart(self, product_name: str):
        button = self.catalog_page.add_to_cart(product_name)
        return button

    @allure.step("Удаляем товар {product_name} из корзины")
    def remove_from_cart(self, product_name: str):
        button = self.catalog_page.remove_from_cart(product_name)
        return button

    @allure.step("Получаем количество товаров в корзине")
    def get_cart_count(self) -> int:
        return self.catalog_page.get_cart_count()

    @allure.step("Получаем счётчик товаров в корзине")
    def cart_badge(self):
        return self.catalog_page.cart_badge

    @allure.step("Получаем количество карточек товаров")
    def get_products_count(self) -> int:
        return self.catalog_page.get_products_count()

    @allure.step("Получаем список названий товаров")
    def get_product_names(self) -> list[str]:
        return self.catalog_page.get_product_names()

    @allure.step("Получаем список цен товаров")
    def get_product_prices(self) -> list[float]:
        return self.catalog_page.get_product_prices()

    @allure.step("Открываем страницу деталей товара: {product_name}")
    def open_product_details(self, product_name: str):
        return self.catalog_page.open_product_details(product_name)
