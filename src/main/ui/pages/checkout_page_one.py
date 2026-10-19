from playwright.sync_api import Page


class CheckoutPageOne:
    URL = "https://www.saucedemo.com/checkout-step-one.html"

    def __init__(self, page: Page):
        self.page = page

        self.enter_first_name = page.get_by_placeholder("First Name")
        self.enter_last_name = page.get_by_placeholder("Last Name")
        self.enter_zip = page.get_by_placeholder("Zip/Postal Code")
        self.button_continue = page.get_by_role("button", name="Continue")
        self.error_text = page.locator('[data-test="error"]')

    def enter_checkout(self, first_name: str, last_name: str, zip_code: str):
        self.enter_first_name.fill(first_name)
        self.enter_last_name.fill(last_name)
        self.enter_zip.fill(zip_code)
        self.button_continue.click()

    def error_text(self) -> str:
        return self.error_text.inner_text()
