from playwright.sync_api import Page


class CheckoutPageTwo:
    URL = "https://www.saucedemo.com/checkout-step-two.html"

    def __init__(self, page: Page):
        self.page = page
        self.item_total = page.locator('.summary_subtotal_label')
        self.tax = page.locator('.summary_tax_label')
        self.total = page.locator('.summary_total_label')
        self.finish_button = page.get_by_role("button", name="Finish")

    def get_item_total_price_from_checkout(self):
        item_total_text = self.item_total.text_content()
        item_total = float(item_total_text.replace("Item total: $", ""))
        return item_total

    def get_sum_tax_price_from_checkout(self):
        tax_text = self.tax.text_content()
        tax = float(tax_text.replace("Tax: $", ""))
        return tax

    def get_sum_total_price_from_checkout(self):
        total_text = self.total.text_content()
        total = float(total_text.replace("Total: $", ""))
        return total

    def click_finish_button(self):
        self.finish_button.click()
