'''
    Product Page
'''
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from utils.best_buy import base_pages
from utils.best_buy.locators import Locators
from utils.best_buy import urls

class ProductPage(base_pages.ProductPage):
    #prod_url = urls.Page.product

    # Change URL to prod_url
    def __init__(self, driver, prod_url):
        #super().__init__(self, driver, prod_url)
        self.prod_url = prod_url
        super().__init__(driver)
        if self.driver.current_url != self.prod_url:
            self.driver.get(self.prod_url)
        else:
            print('Already in product page')

    # this function add to cart
    def add_to_cart(self):
        add_cart_btn = self.get_add_cart_btn(self)
        try: 
            add_cart_btn.click()
            WebDriverWait(self.driver, 0.25).until(EC.presence_of_element_located(Locators.ProductPage.add_btn_animation))
        except:
            return False
        else:
            WebDriverWait(self.driver, 10).until_not(EC.presence_of_element_located(Locators.ProductPage.add_btn_animation))
            try:
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(Locators.ProductPage.cart_popup))
            except:
                if EC.presence_of_element_located(Locators.ProductPage.cart_failed_popup):
                    print('Failed to add to cart. Retrying!!!\n')
                    time.sleep(4)
                return False
            else:
                return True

    # This function check the product availibility (return True if avail)
    def check_avail(self):
        try:
            self.get_add_cart_btn(self)
            #addtocart_btn = driver.find_element_by_css_selector(bb_add_to_cart_css)
        except:
            return False
        else:
            return True
            
    def get_add_cart_btn(self):
        return WebDriverWait(self.driver, 1).until(EC.element_to_be_clickable(Locators.ProductPage.add_cart_btn))
