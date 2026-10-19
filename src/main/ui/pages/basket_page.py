from playwright.sync_api import Page


class BasketPage:
    URL = "https://www.saucedemo.com/cart.html"

    def __init__(self, page: Page):
        self.page = page

        self.item_name = page.locator('[data-test="inventory-item-name"]')
        self.cart_list = page.locator('.cart_list')
        self.cart_items = page.locator('.cart_item')
        self.button_checkout = page.locator('#checkout')
        self.price_items = page.locator('.inventory_item_price')

    def open(self):
        self.page.goto(self.URL)

    def get_item_name(self, product_name: str):
        return self.item_name.filter(has_text=product_name)

    def get_all_cart_items(self):
        return self.item_name.all_inner_texts()

    def remove_item_from_cart(self, product_name: str):
        card = self.cart_items.filter(has_text=product_name)
        button = card.locator("button")
        if button.inner_text() == "Remove":
            button.click()
        return button

    def get_sum_all_price_item_from_cart(self):
        prices_text = self.price_items.all_text_contents()
        prices = [float(p.replace("$", "")) for p in prices_text]
        prices_sum = sum(prices)
        return prices_sum

    def open_checkout(self):
        self.button_checkout.click()
