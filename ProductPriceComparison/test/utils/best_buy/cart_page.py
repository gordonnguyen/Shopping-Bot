from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.best_buy.base_page import BasePage
from utils.best_buy.locators import CartPageLocators
from utils.best_buy.urls import MainUrls


class CartPage(BasePage):
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = MainUrls.cart

    def to_checkout(self):
        self.click(CartPageLocators.to_checkout_btn)
        WebDriverWait(self.driver, 5).until(EC.url_changes(self.url))