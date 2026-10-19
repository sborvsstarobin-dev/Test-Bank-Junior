import allure
from playwright.sync_api import Page
from src.main.ui.pages.basket_page import BasketPage


class BasketSteps:
    def __init__(self, page: Page):
        self.page = page
        self.basket_page = BasketPage(self.page)

    @allure.step("Открываем страницу корзины")
    def open_basket_page(self):
        self.basket_page.open()
        return self

    @allure.step("Получаем товар из корзины {product_name}")
    def get_item_name(self, product_name: str):
        return self.basket_page.get_item_name(product_name)

    @allure.step("Получаем все товары из корзины")
    def get_all_cart_items(self):
        return self.basket_page.get_all_cart_items()

    @allure.step("Удаляем товар {product_name} из корзины")
    def remove_item_from_cart(self, product_name: str):
        return self.basket_page.remove_item_from_cart(product_name)

    @allure.step("Считаем сумму всех товаров в корзине")
    def get_sum_all_price_item_from_cart(self):
        return self.basket_page.get_sum_all_price_item_from_cart()

    @allure.step("Переход на страницу checkout")
    def open_checkout(self):
        self.basket_page.open_checkout()
        return self
