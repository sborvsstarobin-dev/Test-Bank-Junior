from playwright.sync_api import expect
from src.main.ui.steps.catalog_steps import CatalogSteps
from src.main.ui.pages.catalog_page import CatalogPage
import pytest


@pytest.mark.ui
class TestCatalog:
    def test_catalog_count_product(self, auth_page):
        catalog_steps = CatalogSteps(auth_page)
        expect(auth_page).to_have_url(CatalogPage.URL)

        count_products = catalog_steps.get_products_count()
        assert count_products == 6

    def test_sorted_by_name_a_z(self, auth_page):
        catalog_steps = CatalogSteps(auth_page)
        expect(auth_page).to_have_url(CatalogPage.URL)

        names = catalog_steps.sort_items("az").get_product_names()
        assert names == sorted(names), "Товары не отсортированы по имени A-Z"

    def test_sorted_by_name_z_a(self, auth_page):
        catalog_steps = CatalogSteps(auth_page)
        expect(auth_page).to_have_url(CatalogPage.URL)

        names = catalog_steps.sort_items("za").get_product_names()
        assert names == sorted(names, reverse=True), "Товары не отсортированы по имени Z-A"

    def test_sorted_by_price_low_high(self, auth_page):
        catalog_steps = CatalogSteps(auth_page)
        expect(auth_page).to_have_url(CatalogPage.URL)

        prices = catalog_steps.sort_items("lohi").get_product_prices()
        assert prices == sorted(prices), "Товары не отсортированы по цене"

    def test_sorted_by_price_high_low(self, auth_page):
        catalog_steps = CatalogSteps(auth_page)
        expect(auth_page).to_have_url(CatalogPage.URL)

        prices = catalog_steps.sort_items("hilo").get_product_prices()
        assert prices == sorted(prices, reverse=True), "Товары не отсортированы по цене"

    def test_add_to_cart(self, auth_page):
        catalog_steps = CatalogSteps(auth_page)
        expect(auth_page).to_have_url(CatalogPage.URL)

        button = catalog_steps.add_to_cart("Sauce Labs Bike Light")

        expect(button).to_have_text("Remove")
        assert catalog_steps.get_cart_count() == 1

    def test_add_to_cart_onesie(self, auth_page):
        catalog_steps = CatalogSteps(auth_page)
        expect(auth_page).to_have_url(CatalogPage.URL)

        button = catalog_steps.add_to_cart("Sauce Labs Onesie")

        expect(button).to_have_text("Remove")
        assert catalog_steps.get_cart_count() == 1

        button_remove = catalog_steps.remove_from_cart("Sauce Labs Onesie")
        expect(button_remove).to_have_text("Add to cart")
        assert catalog_steps.get_cart_count() == 0

    def test_product_details_onesie(self, auth_page):
        catalog_steps = CatalogSteps(auth_page)
        expect(auth_page).to_have_url(CatalogPage.URL)

        name, price, detail_name, detail_price = catalog_steps.open_product_details("Sauce Labs Onesie")

        assert detail_name == name
        assert detail_price == price

    def test_product_details_jacket(self, auth_page):
        catalog_steps = CatalogSteps(auth_page)
        expect(auth_page).to_have_url(CatalogPage.URL)

        name, price, detail_name, detail_price = catalog_steps.open_product_details("Sauce Labs Fleece Jacket")

        assert detail_name == name
        assert detail_price == price
