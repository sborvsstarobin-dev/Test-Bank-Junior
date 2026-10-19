import allure
from playwright.sync_api import Page
from src.main.ui.pages.checkout_page_one import CheckoutPageOne
from src.main.ui.pages.checkout_page_two import CheckoutPageTwo


class CheckoutSteps:
    def __init__(self, page: Page):
        self.page = page
        self.checkout_page_one = CheckoutPageOne(self.page)
        self.checkout_page_two = CheckoutPageTwo(self.page)

    @allure.step("Заполняем поля ввода на странице checkout-step-one")
    def enter_checkout(self, first_name: str, last_name: str, zip_code: str):
        self.checkout_page_one.enter_checkout(first_name, last_name, zip_code)
        return self

    @allure.step("Получаем сообщение об ошибке при её наличии")
    def get_error_text(self):
        if self.checkout_page_one.error_text.is_visible():
            return self.checkout_page_one.error_text.inner_text()
        return ""

    @allure.step("Считаем сумму товаров Item Total на странице checkout-step-two")
    def get_item_total_price_from_checkout(self):
        item_total = self.checkout_page_two.get_item_total_price_from_checkout()
        return item_total

    @allure.step("Считаем сумму товаров Tax на странице checkout-step-two")
    def get_sum_tax_price_from_checkout(self):
        tax = self.checkout_page_two.get_sum_tax_price_from_checkout()
        return tax

    @allure.step("Считаем сумму товаров Total на странице checkout-step-two")
    def get_sum_total_price_from_checkout(self):
        total = self.checkout_page_two.get_sum_total_price_from_checkout()
        return total

    @allure.step("Кликаем на кнопку Finish")
    def click_finish_button(self):
        self.checkout_page_two.click_finish_button()
        return self
