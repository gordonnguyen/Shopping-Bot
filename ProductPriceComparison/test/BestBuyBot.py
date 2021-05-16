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

from utils.best_buy import locators
from utils.best_buy.product_page import ProductPage
from utils.best_buy.cart_page import CartPage
from utils.best_buy.sign_in_page import SignInPage
from utils.best_buy.urls import MainUrls

import datetime
import time
#import notifier

# CUSTOMS
LINE = '\n'+'='*50


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
#product_url = 'https://www.bestbuy.com/site/sony-wh-ch510-wireless-on-ear-headphones-black/6359775.p?skuId=6359775'
product_url = 'https://www.bestbuy.com/site/macbook-air-13-3-laptop-apple-m1-chip-8gb-memory-256gb-ssd-latest-model-gold/6418599.p?skuId=6418599'


BB_HOME_URL = 'https://www.bestbuy.com/'
BB_SIGNIN_URL = 'https://www.bestbuy.com/identity/global/signin'
BB_CHECKOUT_URL = 'https://www.bestbuy.com/checkout/r/fast-track'
BB_PAYMENT_URL = 'https://www.bestbuy.com/checkout/r/payment'
BB_CART_URL = 'https://www.bestbuy.com/cart'
BB_2FA_URL_PATTERN = 'identity/signin'
BB_CHECKOUT_FINAL_URL = 'https://www.bestbuy.com/checkout/r/fast-track'


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
    order_placed = False

    driver = launch_chrome()
    '''
    prod_page_check_add_cart(driver)
    cart_page(driver)
    order_placed = checkout(driver)
    #if order_placed:
        #notify_all()

    time.sleep(final_viewing_time)
    driver.close()
    '''
    add_product(driver)
    cart_page = CartPage(driver)
    cart_page.to_main_url()
    cart_page.to_checkout()
    sign_in(driver)
    print(LINE)
    print('All done!!!')
    while True:
        pass

def add_product(driver):
    order_placed = False
    prod_page = ProductPage(driver, product_url)
    avail_count = 0

    while True:
        prod_avail = prod_page.check_avail()
        if prod_avail:
            print(LINE)
            print_current_time()
            print('Product is available!!!\n')
            break
        else:
            avail_count += 1
            if avail_count == 1:
                print(LINE)
                print('Product currently unavailable! Refreshing page...\n')
            elif avail_count%10 == 0:
                print(LINE)
                print_current_time()
                print('Still unavailable! Retries count:', avail_count, '\n<Refreshing page again...>\n')
            prod_page.driver.get(product_url)

    while True:
        prod_page.add_to_cart()
        add_cart_count = 1
        if prod_page.is_added == True:
            print(LINE)
            print_current_time()
            print('Product added to cart!')
            break
        else:
            if add_cart_count == 1:
                print(LINE)
                print_current_time()
                print('Button stuck. Retrying!\n')
            else:
                print(LINE)
                print('Failed to add to cart')
            add_cart_count = 0

def sign_in(driver):
    sign_in_page = SignInPage(driver)
    if MainUrls.f2a_pattern in driver.current_url:
        print(LINE + '\nF2A Sign in page: True')
    else:
        print('Signin page not found!')
        sign_in_page.to_main_url()
    sign_in_page.sign_in()

    print(LINE)
    print_current_time()
    print('Signed in successfully!')
    
    if sign_in_page.is_2fa():
        print(LINE)
        print('Prefilling 2FA phone number...')
        sign_in_page.prefill_2fa()
    else:
        print(LINE + '\n2FA not detected!')

def checkout(driver):
    checkout_page = CheckOutPage

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