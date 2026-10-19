from playwright.sync_api import expect
from src.main.ui.pages.basket_page import BasketPage
from src.main.ui.pages.catalog_page import CatalogPage
from src.main.ui.pages.checkout_page_one import CheckoutPageOne
from src.main.ui.pages.checkout_page_two import CheckoutPageTwo
from src.main.ui.steps.catalog_steps import CatalogSteps
from src.main.ui.steps.checkout_steps import CheckoutSteps
from src.main.ui.steps.basket_steps import BasketSteps
import pytest


@pytest.mark.ui
class TestCheckoutCart:
    def test_checkout_cart(self, auth_page):
        catalog_steps = CatalogSteps(auth_page)
        basket_steps = BasketSteps(auth_page)
        checkout_steps = CheckoutSteps(auth_page)

        expect(auth_page).to_have_url(CatalogPage.URL)

        catalog_steps.add_to_cart('Sauce Labs Fleece Jacket')
        catalog_steps.add_to_cart('Sauce Labs Bolt T-Shirt')
        catalog_steps.open_cart()

        expect(auth_page).to_have_url(BasketPage.URL)

        item_names = basket_steps.get_all_cart_items()
        assert "Sauce Labs Fleece Jacket" in item_names
        assert "Sauce Labs Bolt T-Shirt" in item_names

        prices_sum_from_cart = basket_steps.get_sum_all_price_item_from_cart()
        basket_steps.open_checkout()
        expect(auth_page).to_have_url(CheckoutPageOne.URL)

        checkout_steps.enter_checkout("Alex", "Kotl", "1111")
        expect(auth_page).to_have_url(CheckoutPageTwo.URL)

        item_total_text = checkout_steps.get_item_total_price_from_checkout()
        print(item_total_text, "- Общая цена без налогов")
        assert item_total_text == prices_sum_from_cart

        tax_text = checkout_steps.get_sum_tax_price_from_checkout()
        print(tax_text, "- Налоги")

        final_sum_price = item_total_text + tax_text
        print(final_sum_price, "- Общая цена с налогами")

        total_text = checkout_steps.get_sum_total_price_from_checkout()
        print(total_text, "- Финальная стоимость")
        assert total_text == final_sum_price

        checkout_steps.click_finish_button()

        expect(auth_page).to_have_url("https://www.saucedemo.com/checkout-complete.html")

        thank_text = auth_page.locator('.complete-header', has_text="Thank you for your order!")
        expect(thank_text).to_be_visible()

    def test_checkout_invalid_last_name(self, auth_page):
        catalog_steps = CatalogSteps(auth_page)
        basket_steps = BasketSteps(auth_page)
        checkout_steps = CheckoutSteps(auth_page)

        expect(auth_page).to_have_url(CatalogPage.URL)

        catalog_steps.add_to_cart('Sauce Labs Backpack')
        catalog_steps.open_cart()

        expect(auth_page).to_have_url(BasketPage.URL)

        item_names = basket_steps.get_all_cart_items()
        assert "Sauce Labs Backpack" in item_names

        basket_steps.open_checkout()
        expect(auth_page).to_have_url(CheckoutPageOne.URL)

        checkout_steps.enter_checkout("Alex", "", "1111")

        assert "Error: Last Name is required" in checkout_steps.get_error_text()
