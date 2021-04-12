"""
Made by: Gordon Nguyen
Updated as of: 03-2021
"""

from copy import Error
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import utils.best_buy.urls
from utils.best_buy.locators import Locators
from utils.best_buy.product_page import ProductPage

import datetime
import time
#import notifier

# Configuration
shipping = False
express_mode = False # Ignore shipping option. Checkout ASAP
payment_method_ready = True
cvv_num = ''
BB_checkout_2fa = True
final_viewing_time = 60*60

# BESTBUY PAGE URLS:
product_name = 'RTX 3060 Ti (BestBuy)'
#product_url = 'https://www.bestbuy.com/site/nvidia-geforce-rtx-3060-ti-8gb-gddr6-pci-express-4-0-graphics-card-steel-and-black/6439402.p?skuId=6439402'
#product_url = 'https://www.bestbuy.com/site/dell-inspiron-15-6-inch-fhd-touch-laptop-amd-ryzen-5-12gb-ram-256-gb-ssd-1-tb-hdd-black/6438338.p?skuId=6438338'
#product_url = 'https://www.bestbuy.com/site/apple-watch-se-gps-40mm-silver-aluminum-case-with-white-sport-band-silver/6215915.p?skuId=6215915'
#product_url = 'https://www.bestbuy.com/site/pny-nvidia-geforce-gt-1030-2gb-gddr5-pci-express-3-0-graphics-card-black/5901353.p?skuId=5901353'
#product_url = 'https://www.bestbuy.com/site/wd-easystore-480gb-solid-state-drive-for-laptops/6411192.p?skuId=6411192'
product_url = 'https://www.bestbuy.com/site/sony-wh-ch510-wireless-on-ear-headphones-black/6359775.p?skuId=6359775'
#product_url = 'https://www.bestbuy.com/site/macbook-air-13-3-laptop-apple-m1-chip-8gb-memory-256gb-ssd-latest-model-gold/6418599.p?skuId=6418599'


BB_HOME_URL = 'https://www.bestbuy.com/'
BB_SIGNIN_URL = 'https://www.bestbuy.com/identity/global/signin'
BB_CHECKOUT_URL = 'https://www.bestbuy.com/checkout/r/fast-track'
BB_PAYMENT_URL = 'https://www.bestbuy.com/checkout/r/payment'
BB_CART_URL = 'https://www.bestbuy.com/cart'
BB_2FA_URL_PATTERN = 'identity/signin'
BB_CHECKOUT_FINAL_URL = 'https://www.bestbuy.com/checkout/r/fast-track'

''' BESTBUY SELECTORS '''
# PRODUCT PAGE:
'''
BB_PRICE_HTML_SELECTOR = ('#prcIsum', '#mm-saleDscPrc', '#prcIsum_bidPrice')
BB_NAME_HTML_SELECTOR = '#itemTitle'
BB_2FA_CONTINUE_XPATH = '/html/body/div[1]/div/section/main/div[2]/div[1]/div/div/div/form/div[3]/button'
BB_ADD_TO_CART_XPATH = '/html/body/div[3]/main/div[2]/div/div[1]/div[3]/div[2]/div/div[2]/div[1]/div/div/div/button'
bb_add_to_cart_css = '.btn.btn-primary.btn-lg.btn-block.btn-leading-ficon.add-to-cart-button'
BB_CART_POPUP_XPATH = '/html/body/div[7]/div'
BB_CART_POPUP_CSS_SELECTOR = 'span.added-to-cart'
BB_CART_FAILED_CSS = 'div > div > div.c-alert-content'
'''

# CART PAGE:
BB_TO_CHECKOUT_BTN_CSS = 'div.checkout-buttons__checkout > button'

# CHECKOUT PAGE:
BB_CHECKOUT = "#cartApp > div.page-spinner.page-spinner--out > div.large-view.size-l > div > div.fluid-large-view > div.fluid-large-view__upper-container > section.fluid-large-view__sidebar > div > div > div.order-summary__checkout-buttons-container > div > div.checkout-buttons__checkout > button"
BB_SHIPPING_RADIO_XPATH = '//*[@id="cartApp"]/*div[2]/div[1]/div/div'
BB_SHIPPING_OPTION_XPATH = '//*[@id="checkoutApp"]/div[2]/div[1]/div[1]/main/div[2]/div[2]/form/section/div/div[1]/div/div/section/div[2]/div[2]/div[2]/div/div/a'

BB_SHIPPING_OPTION_LINKTEXT = 'Switch to Shipping'
BB_SHIPPING_OPTION_CSS_SELECTOR = 'a.ispu-card__switch'
BB_SHIPPING_RADIO_CSS_SELECTOR = 'div.availability__entry.availability--unselected.availability--remove-z-index > div > div'
BB_CONTINUE_PAYMENT_XPATH = '//*[@id="checkoutApp"]/div[2]/div[1]/div[1]/main/div[2]/div[2]/form/section/div/div[2]/div/div/button'

BB_PLACE_ORDER_XPATH = '//*[@id="checkoutApp"]/div[2]/div[1]/div[1]/main/div[2]/div[3]/div/section/div[4]/button'

BB_PLACE_ORDER_CSS_SELECTOR = '.btn.btn-lg.btn-block.btn-primary'
BB_CREDIT_CVV_ID = 'credit-card-cvv'

BB_CHANGE_PICKUP_STORE = 'a.btn-default-link.link-styled-button.ispu-display__change'
BB_PICKUP_STORE_ID = 'store-213-fulfillment'        # Sharptown 8210 S Gessner Dr Houston, TX 77036
BB_PICKUP_STORE_CSS = '#store-213-fulfillment-wrapper > a'
BB_SELECT_STORE_XPATH = '//*[@id="sc-store-availability-modal"]/div/div/div[2]/div/div/div[2]/div[3]/div[3]/div'


''' '''


def main():
    '''
    order_placed = False
    driver = launch_chrome()
    prod_page_check_add_cart(driver)
    cart_page(driver)
    order_placed = checkout(driver)
    #if order_placed:
        #notify_all()

    time.sleep(final_viewing_time)
    driver.close()
    '''
    add_product()

def add_product():
    order_placed = False
    driver = launch_chrome()
    prod_page = ProductPage(driver, product_url)
    avail_count = 0

    while True:
        prod_avail = prod_page.check_avail()
        if prod_avail:
            print_current_time()
            print('Product is available!!!\n')
            break
        else:
            avail_count += 1
            if avail_count == 1:
                print('Product currently unavailable! Refreshing page...\n')
            elif avail_count%10 == 0:
                print_current_time()
                print('Still unavailable! Retries count:', avail_count, '\n<Refreshing page again...>\n')
            prod_page.driver.get(product_url)

    while True:
        add_cart_count = 1
        is_added_to_cart = prod_page.add_to_cart()
        if is_added_to_cart:
            print('Product added to cart!')
            break
        else:
            if add_cart_count == 1:
                print_current_time()
                print('Button stuck. Retrying!\n')
            else:
                print('Failed to add to cart')
            add_cart_count = 0




def print_current_time():
    print(datetime.datetime.now().strftime('< %m/%d/%Y - %H:%M:%S >'))

def launch_chrome():
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "eager"
    #chrome_path = 'chromedriver'  # executable_path=chrome_path, 
    options = Options()
    options.add_argument("--log-level=3")   # Disable driver minor error logs
    #options.add_experimental_option("detach", True)
    return webdriver.Chrome(desired_capabilities=caps, options=options)

def launch_fire_fox():
    return webdriver.Firefox()

'''
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
    prod_url = product_url

    # SELECTORS
    BB_PRICE_HTML_SELECTOR = ('#prcIsum', '#mm-saleDscPrc', '#prcIsum_bidPrice')
    BB_NAME_HTML_SELECTOR = '#itemTitle'
    BB_2FA_CONTINUE_XPATH = '/html/body/div[1]/div/section/main/div[2]/div[1]/div/div/div/form/div[3]/button'
    BB_ADD_TO_CART_XPATH = '/html/body/div[3]/main/div[2]/div/div[1]/div[3]/div[2]/div/div[2]/div[1]/div/div/div/button'
    bb_add_to_cart_css = '.btn.btn-primary.btn-lg.btn-block.btn-leading-ficon.add-to-cart-button'
    BB_CART_POPUP_XPATH = '/html/body/div[7]/div'
    BB_CART_POPUP_CSS_SELECTOR = 'span.added-to-cart'
    BB_CART_FAILED_CSS = 'div > div > div.c-alert-content'


    ### Product Page ###
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
            WebDriverWait(self.driver, 0.25).until(EC.presence_of_element_loca.ProductPage.add_btn_animation))
        except:
            return False
        else:
            WebDriverWait(self.driver, 10).until_not(EC.presence_of_element_loca.ProductPage.add_btn_animation))
            try:
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_loca.ProductPage.cart_popup))
            except:
                if EC.presence_of_element_loca.ProductPage.cart_failed_popup):
                    print_current_time
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
        return WebDriverWait(self.driver, 1).until(EC.element_to_be_clicka.ProductPage.add_cart_btn))
'''

'''
class CartPage(BasePage):
    def __init__(self, driver):
        self.driver = driver

    def to_checkout(self):
        is_signed_in = False

        self.driver.get(BB_CART_URL)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, BB_TO_CHECKOUT_BTN_CSS)))
        self.driver.find_element_by_css_selector(BB_TO_CHECKOUT_BTN_CSS).click()
        is_signed_in = SignInPage.sign_in(self.driver, is_signed_in)
        if is_signed_in:
            print('Signed in successfully!')

class SignInPage(BasePage):
    BB_email_selector = 'fld-e'
    BB_password_selector = 'fld-p1'
    BB_signin_selector = 'cia-form__controls '  # Used for 2fa continue
    BB_verify_field_ID = 'verificationCode'
    BB_2fa_text_option_ID = 'sms-radio'
    BB_2fa_text_option_XPATH = '/html/body/div[1]/div/section/main/div[2]/div[1]/div/div/div/div/form/fieldset/fieldset/div[3]/label/div/i'
    BB_2fa_email_option_ID = 'email-radio'
    BB_sms_4digits_ID = 'smsDigits'

    def __init__(self):
        self.BB_email = 'maixanh45@yahoo.com'
        self.BB_password = '@Nhan021400'
        self.BB_sms_4digits = '9386'

    def sign_in(self, driver, is_signed_in):
        WebDriverWait(driver, 10).until(EC.url_contains(BB_2FA_URL_PATTERN))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, self.BB_signin_selector)))
        current_signin_url = driver.current_url
        print('Current sign in url: ', current_signin_url)
        if BB_2FA_URL_PATTERN in current_signin_url:
            print('Sign in page: True')
        else:
            print('Failed to detect sign in')

        if is_signed_in == False:
            # Fill email and password fields
            driver.find_element_by_id(self.BB_email_selector).send_keys(self.BB_email)
            driver.find_element_by_id(self.BB_password_selector).send_keys(self.BB_password)
            # Submit / Signin button
            driver.find_element_by_class_name(self.BB_signin_selector).click()
        WebDriverWait(driver, 10).until(EC.url_changes(current_signin_url))

        current_2fa_url = driver.current_url
        print('Current 2FA url: ', current_2fa_url)
        if BB_2FA_URL_PATTERN in current_2fa_url:
            print_current_time()
            print('2FA Detected\n')
            try:
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, self.BB_2fa_text_option_ID)))
            except:
                print('May not be a 2FA page')
            else:
                # Select and Enter sms digits
                print('Require user interaction!')
                driver.find_element_by_xpath(self.BB_2fa_text_option_XPATH).click()
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, self.BB_sms_4digits_ID)))
                driver.find_element_by_id(self.BB_sms_4digits_ID).send_keys(self.BB_sms_4digits)
                driver.find_element_by_class_name(self.BB_signin_selector).click()

                # Wait for user to type 2fa code
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, self.BB_verify_field_ID)))
                WebDriverWait(driver, 240).until_not(EC.presence_of_element_located((By.ID, self.BB_verify_field_ID)))
        else:
            print('No 2FA detected!\n')
'''

### Checkout Page ###
class CheckOutPage():
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

    def select_shipping():
        # Switch to shipping option (if available)
        if shipping:
            try:
                driver.find_element_by_link_text(BB_SHIPPING_OPTION_LINKTEXT).click()
            except:
                print('Shipping already set or unable to select shipping option!\n')
                select_pickup_store(driver)
            else:
                print('Selected shipping option.\n')
        else:
            select_pickup_store(driver)

    def fill_payment(self):
        self.checkout_pg_wait(driver)
        if payment_method_ready:
            # Credit Card CVV Code
            driver.find_element_by_id(BB_CREDIT_CVV_ID).send_keys(cvv_num)

    # Place order
    def place_order(self):
        current_payment_url = driver.current_url
        for retry in range(3):
            try:
                checkout_pg_wait(driver)
                driver.find_element_by_css_selector(BB_PLACE_ORDER_CSS_SELECTOR).click()
            except:
                print('Unable to place the order!\n Retrying... \n')
            else:
                break
        
        try:
            WebDriverWait(driver, 20).until(EC.url_changes(current_payment_url))
        except:
            print_current_time()
            print('Credit card not valid! Please check payment option.')
            return False
        else:
            print_current_time()
            print('Success! Order has been placed.\n')
            return True

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
class bb_notify:
    def __init__(self, title, message):
        self.title = title
        self.message = message
        notifier.notifyNative(title, message)

class order_placed(bb_notify):


def notify_all():
    title = '(BestBuy) Order has been automatically placed!'
    message = 'Congratulation! '+product_name+' is placed.'
    notifier.notifyDesktop(title, message)
    notifier.notifyPhoneEmail(title, message)
'''


main()