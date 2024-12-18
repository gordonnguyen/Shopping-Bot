'''
    Product Page
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from base_page import BasePage
from locators import Locators as Loc
from urls import BBUrls as url

class ProductPage(BasePage):
    prod_url = url.product

    # Change URL to prod_url
    def __init__(self, driver):
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
            WebDriverWait(self.driver, 0.25).until(EC.presence_of_element_located(Loc.ProductPage.add_btn_animation))
        except:
            return False
        else:
            WebDriverWait(self.driver, 10).until_not(EC.presence_of_element_located(Loc.ProductPage.add_btn_animation))
            try:
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(Loc.ProductPage.cart_popup))
            except:
                if EC.presence_of_element_located(Loc.ProductPage.cart_failed_popup):
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
        return WebDriverWait(self.driver, 1).until(EC.element_to_be_clickable(Loc.ProductPage.add_cart_btn))
