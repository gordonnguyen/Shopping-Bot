from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.best_buy.base_page import BasePage
from utils.best_buy.locators import CheckOutPageLocators
from utils.best_buy.urls import MainUrls

class CheckOutPage(BasePage):
    BB_success_url = 'https://www.bestbuy.com/checkout/r/thank-you'
    '''
    # Check if BB Checkout 2FA is active:
    try:
        WebDriverWait(driver, 10).until(EC.url_matches('https://www.bestbuy.com/identity/signin'))
    except:
        WebDriverWait(driver, 10).until(EC.url_matches(BB_CHECKOUT_URL))
    else:
        is_signed_in = sign_in(driver, is_signed_in)
        if is_signed_in:
            print('Signed in successfully')
        else:
            print('Unable to sign in!')
    '''
    # Wait until driver load properly
    #checkout_pg_wait(driver)

    def __init__(self, driver=None, cvv_num=''):
        super().__init__(driver)
        self.__cvv_num = cvv_num


    def select_delivery_option(self, delivery_option='', store_id=''):
        # Switch to shipping option (if available)
        if delivery_option == 'shipping':
            #WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(CheckOutPageLocators.shipping_radio_btn)).click()
            try:
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(CheckOutPageLocators.shipping_card_frame))
            except:
                try:
                    self.click(CheckOutPageLocators.shipping_radio_btn)
                except:
                    return False
                else:
                    return True
            else:
                return True

        elif delivery_option == 'pickup':
            try:
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(CheckOutPageLocators.pickup_card_frame))
            except:
                try:
                    self.click(CheckOutPageLocators.pickup_radio_btn)
                except:
                    return False
                else:
                    # Change pickup store using store id
                    try:
                        if store_id != '':
                            self.click(CheckOutPageLocators.change_store_btn)
                            self.click(CheckOutPageLocators.pickup_store_id)
                            self.click(CheckOutPageLocators.select_store_btn)
                    except:
                        return False
                    else:
                        return True
            else:
                return True


    def fill_payment(self):
        # Fill Credit Card CVV Code
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(CheckOutPageLocators.credit_cvv)).send_keys(self.__cvv_num)
        #self.driver.find_element_by_id(BB_CREDIT_CVV_ID)

    # Place order
    def place_order(self):
        try:
            #driver.find_element_by_css_selector(BB_PLACE_ORDER_CSS_SELECTOR).click()
            self.click(CheckOutPageLocators.place_order_btn)
        except:
            return False
        else:
            return True
        
    def check_order_success(self):
        try:
            WebDriverWait(self.driver, 30).until(EC.url_matches(MainUrls.checkout_completed))
        except:
            return False
        else:
            return True

    '''
    def select_pickup_store(driver):
        try:
            driver.find_element_by_css_selector(BB_CHANGE_PICKUP_STORE).click()
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, BB_PICKUP_STORE_ID)))
            driver.find_element_by_css_selector(BB_PICKUP_STORE_CSS).click()
            driver.find_element_by_xpath(BB_SELECT_STORE_XPATH).click()
        except:
            print('Unable to select pickup store!')
        else:
            print('Selected chosen store')

    def checkout_pg_wait(driver):
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, BB_PLACE_ORDER_CSS_SELECTOR)))
    '''
