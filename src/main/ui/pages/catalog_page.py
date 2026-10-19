from playwright.sync_api import Page


class CatalogPage:
    URL = "https://www.saucedemo.com/inventory.html"

    def __init__(self, page: Page):
        self.page = page

        self.burger_menu_button = page.get_by_role("button", name="Open Menu")
        self.logout_link = page.locator("#logout_sidebar_link")
        self.product_cards = page.locator(".inventory_item")
        self.sort_select = page.locator(".product_sort_container")
        self.item_names_catalog = page.locator(".inventory_item_name")
        self.prices_text_catalog = page.locator(".inventory_item_price")
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.cart_link = page.locator(".shopping_cart_link")

    def open(self):
        self.page.goto(self.URL)

    def logout(self):
        self.burger_menu_button.click()
        self.logout_link.click()

    def sort_catalog_items(self, option: str):
        self.sort_select.select_option(option)

    def open_cart(self):
        self.cart_link.click()

    def cart_badge(self):
        return self.cart_badge

    def add_to_cart(self, product_name: str):
        card = self.product_cards.filter(has_text=product_name)
        button = card.locator("button")
        if button.inner_text() == "Add to cart":
            button.click()
        return button

    def remove_from_cart(self, product_name: str):
        card = self.product_cards.filter(has_text=product_name)
        button = card.locator("button")
        if button.inner_text() == "Remove":
            button.click()
        return button

    def get_cart_count(self) -> int:
        if self.cart_badge.is_visible():
            return int(self.cart_badge.inner_text())
        return 0

    def get_products_count(self) -> int:
        return self.product_cards.count()

    def get_product_names(self) -> list[str]:
        return self.product_cards.locator(".inventory_item_name").all_text_contents()

    def get_product_prices(self) -> list[float]:
        prices_text = self.product_cards.locator(".inventory_item_price").all_text_contents()
        return [float(p.replace("$", "")) for p in prices_text]

    def open_product_details(self, product_name: str):
        card = self.product_cards.filter(has_text=product_name)
        name = card.locator(".inventory_item_name").inner_text()
        price_text = card.locator(".inventory_item_price").inner_text()
        price = float(price_text.replace("$", ""))

        card.locator(".inventory_item_name").click()
        detail_name = self.page.locator(".inventory_details_name").inner_text()
        detail_price_text = self.page.locator(".inventory_details_price").inner_text()
        detail_price = float(detail_price_text.replace("$", ""))

        self.page.go_back()
        return name, price, detail_name, detail_price
