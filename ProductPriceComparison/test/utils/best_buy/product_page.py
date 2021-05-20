'''
    Product Page
'''
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from utils.best_buy.base_page import BasePage
from utils.best_buy.locators import ProductPageLocators

class ProductPage(BasePage):
    '''
        Product Page
    '''
    # Change URL to prod_url
    def __init__(self, driver, prod_url):
        super().__init__(driver)
        self.prod_url = prod_url
        if self.driver.current_url != self.prod_url:
            self.driver.get(self.prod_url)
        else:
            print('Already in product page')

    # this function add to cart and check if its succesful
    def add_to_cart(self):
        try: 
            print('Adding to cart...')
            self.add_cart_btn.click()
            WebDriverWait(self.driver, 0.2).until(EC.presence_of_element_located(ProductPageLocators.add_btn_animation))
        except:
            self.err_msg = 'Currently in queue'
            print('Click error!')
            self.is_added = False
        else:
            print('Button clicked')
            self.wait.until_not(EC.presence_of_element_located(ProductPageLocators.add_btn_animation))
            
            try:
                print('Checking popup')
                self.wait.until(EC.presence_of_element_located(ProductPageLocators.cart_popup))
            except:
                print('Click unsuccessful!')
                self.is_added = False
            else:
                print('Click successful!')
                self.is_added = True

    '''
    # this function add to cart
    def add_to_cart(self):
        # self.add_cart_btn = self.get_add_cart_btn(self)
        try:
            self.add_cart_btn.click()
            #self.click(ProductPageLocators.add_cart_btn)
        except:
            #self.err_msg = 
            return False
        else:
            return True
    '''


    # This function check the product availibility (return True if avail)
    def check_avail(self):
        try:
            self.add_cart_btn = WebDriverWait(self.driver, 1).until(EC.visibility_of_element_located(ProductPageLocators.add_cart_btn))
        except:
            return False
        else:
            return True
            
    #def get_add_cart_btn(self):
        #return WebDriverWait(self.driver, 1).until(EC.element_to_be_clickable(Locators.ProductPage.add_cart_btn))


    '''
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
    '''
