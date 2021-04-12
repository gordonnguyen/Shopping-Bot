'''
    Base Page class for Best Buy Bot
'''
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.best_buy.base_page import BasePage
from utils.best_buy.locators import Locators
from utils.best_buy import urls

class BasePage():
    
    # Initialize browser
    def __init__(self, driver):
        self.driver = driver

    # Wait for element to be clickable and click
    def click(self, by_locator):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(by_locator)).click()

    # Enter text
    def enter_text(self, by_locator, text):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(by_locator)).send_keys(text)

    def check_url(self, target_url):
        if self.driver.current_url == target_url:
            return True

class ProductPage(BasePage):
    #prod_url = urls.Page.product

    # Change URL to prod_url
    def __init__(self, driver, prod_url):
        super().__init__(self, driver)
        self.prod_url = prod_url

    # this function add to cart
    def add_to_cart(self):
        # self.add_cart_btn = self.get_add_cart_btn(self)
        try:
            self.add_cart_btn = self.click(Locators.ProductPage.add_cart_btn)
        except:
            return False
        else:
            return True

    # This function check the product availibility (return True if avail)
    def check_avail(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(Locators.ProductPage.add_cart_btn))
            #self.get_add_cart_btn(self)
            #addtocart_btn = driver.find_element_by_css_selector(bb_add_to_cart_css)
        except:
            return False
        else:
            return True
            
    #def get_add_cart_btn(self):
        #return WebDriverWait(self.driver, 1).until(EC.element_to_be_clickable(Locators.ProductPage.add_cart_btn))