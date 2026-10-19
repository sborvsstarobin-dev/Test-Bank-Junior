from playwright.sync_api import Page


class LoginPage:
    URL = "https://www.saucedemo.com"

    def __init__(self, page: Page):
        self.page = page
        self.enter_username = page.get_by_role("textbox", name="Username")
        self.enter_password = page.get_by_role("textbox", name="Password")
        self.login_button = page.get_by_role("button", name="Login")
        self.error_message = page.locator("h3[data-test='error']")

    def open(self):
        self.page.goto(self.URL)

    def login(self, username: str, password: str):
        self.enter_username.fill(username)
        self.enter_password.fill(password)
        self.login_button.click()

    def get_error_text(self) -> str:
        return self.error_message.inner_text()
