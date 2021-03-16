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
import datetime
import time
#import Notifier

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

''' BESTBUY SELECTORS '''
# PRODUCT PAGE:
BB_PRICE_HTML_SELECTOR = ('#prcIsum', '#mm-saleDscPrc', '#prcIsum_bidPrice')
BB_NAME_HTML_SELECTOR = '#itemTitle'
BB_2FA_CONTINUE_XPATH = '/html/body/div[1]/div/section/main/div[2]/div[1]/div/div/div/form/div[3]/button'
BB_ADD_TO_CART_XPATH = '/html/body/div[3]/main/div[2]/div/div[1]/div[3]/div[2]/div/div[2]/div[1]/div/div/div/button'
BB_ADD_TO_CART_CSS = '.btn.btn-primary.btn-lg.btn-block.btn-leading-ficon.add-to-cart-button'
BB_CART_POPUP_XPATH = '/html/body/div[7]/div'
BB_CART_POPUP_CSS_SELECTOR = 'span.added-to-cart'
BB_CART_FAILED_CSS = 'div > div > div.c-alert-content'

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
    order_placed = False
    browser = launchBrowser()
    prod_page_check_add_cart(browser)
    cart_page(browser)
    order_placed = checkout(browser)
    if order_placed:
        NotifyOrderPlaced()

    time.sleep(final_viewing_time)
    while True:
        pass

def print_current_time():
    print(datetime.datetime.now().strftime('< %m/%d/%Y - %H:%M:%S >'))

def launchBrowser():
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "eager"
    chrome_path = 'chromedriver'
    options = Options()
    #options.add_experimental_option("detach", True)
    return webdriver.Chrome(executable_path=chrome_path, desired_capabilities=caps, chrome_options=options)

def sign_in(browser, is_signed_in):
    BB_email_selector = 'fld-e'
    BB_email = 'maixanh45@yahoo.com'
    BB_password_selector = 'fld-p1'
    BB_password = '@Maixanh45'
    BB_sms_4digits = '9386'

    BB_signin_selector = 'cia-form__controls '  # Used for 2fa continue
    BB_verify_field_ID = 'verificationCode'
    BB_2fa_text_option_ID = 'sms-radio'
    BB_2fa_text_option_XPATH = '/html/body/div[1]/div/section/main/div[2]/div[1]/div/div/div/div/form/fieldset/fieldset/div[3]/label/div/i'
    BB_2fa_email_option_ID = 'email-radio'
    BB_sms_4digits_ID = 'smsDigits'
    ####
    

    WebDriverWait(browser, 10).until(EC.url_contains(BB_2FA_URL_PATTERN))
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, BB_signin_selector)))
    current_signin_url = browser.current_url
    print('Current sign in url: ', current_signin_url)
    if BB_2FA_URL_PATTERN in current_signin_url:
        print('Sign in page: True')
    else:
        print('Failed to detect sign in')

    if is_signed_in == False:
        # Fill email and password fields
        browser.find_element_by_id(BB_email_selector).send_keys(BB_email)
        browser.find_element_by_id(BB_password_selector).send_keys(BB_password)
        # Submit / Signin button
        browser.find_element_by_class_name(BB_signin_selector).click()
    WebDriverWait(browser, 10).until(EC.url_changes(current_signin_url))

    current_2fa_url = browser.current_url
    print('Current 2FA url: ', current_2fa_url)
    if BB_2FA_URL_PATTERN in current_2fa_url:
        print_current_time()
        print('2FA Detected\n')
        try:
            WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.ID, BB_2fa_text_option_ID)))
        except:
            print('May not be a 2FA page')
        else:
            # Select and Enter sms digits
            print('Require user interaction!')
            browser.find_element_by_xpath(BB_2fa_text_option_XPATH).click()
            WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.ID, BB_sms_4digits_ID)))
            browser.find_element_by_id(BB_sms_4digits_ID).send_keys(BB_sms_4digits)
            browser.find_element_by_class_name(BB_signin_selector).click()

             # Wait for user to type 2fa code
            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, BB_verify_field_ID)))
            WebDriverWait(browser, 240).until_not(EC.presence_of_element_located((By.ID, BB_verify_field_ID)))
    else:
        print('No 2FA detected!\n')

    
    '''
    if BB_checkout_2fa == True:
        try:
            # Wait for user to type 2fa code
            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, BB_verify_field_ID)))
            WebDriverWait(browser, 120).until_not(EC.presence_of_element_located((By.ID, BB_verify_field_ID)))
        except:
            return False
        else:
            return True
    else:
        try:
            WebDriverWait(browser, 10).until(EC.url_changes(current_signin_url))
        except:
            return False
        else:
            return True
    '''




### Product Page ###
def prod_page_check_add_cart(browser):
    browser.get(product_url)

    # Check product is available
    addtocart_btn = check_prod_avail(browser)

    is_added_to_cart = try_add_to_cart(addtocart_btn, browser)
    if is_added_to_cart:
        print('Product added to cart!')
    else:
        print('Failed to add to cart')

def try_add_to_cart(addtocart_btn, browser):
    
    add_to_cart_count = 1
    while True: 
        if add_to_cart_count == 1:
            print('Adding to cart...')

        try: 
            addtocart_btn.click()
            WebDriverWait(browser, 0.25).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.spinner.spinner-sm')))
        except:
            if add_to_cart_count == 1:
                print_current_time()
                print('Button stuck. Retrying!\n')
            add_to_cart_count = 0
        else:
            WebDriverWait(browser, 10).until_not(EC.presence_of_element_located((By.CSS_SELECTOR, '.spinner.spinner-sm')))
            try:
                WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, BB_CART_POPUP_CSS_SELECTOR)))
            except:
                if EC.presence_of_element_located((By.CSS_SELECTOR, BB_CART_FAILED_CSS)):
                    print_current_time
                    print('Failed to add to cart. Retrying!!!\n')
                    time.sleep(4)
            else:
                return True

def check_prod_avail(browser):
    avail_count = 0
    while True:
        try:
            WebDriverWait(browser, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, BB_ADD_TO_CART_CSS)))
            addtocart_btn = browser.find_element_by_css_selector(BB_ADD_TO_CART_CSS)
        except:
            avail_count += 1
            if avail_count == 1:
                print('Product currently unavailable! Refreshing page...\n')
            elif avail_count%10 == 0:
                print_current_time()
                print('Still unavailable! Retries count:', avail_count, '\n<Refreshing page again...>\n')
            browser.get(product_url)
        else:
            print_current_time()
            print('Product is available!!!\n')
            return addtocart_btn

def cart_page(browser):
    is_signed_in = False

    browser.get(BB_CART_URL)
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, BB_TO_CHECKOUT_BTN_CSS)))
    browser.find_element_by_css_selector(BB_TO_CHECKOUT_BTN_CSS).click()
    is_signed_in = sign_in(browser, is_signed_in)
    if is_signed_in:
        print('Signed in successfully!')

### Checkout Page ###
def checkout(browser):
    '''
    # Check if BB Checkout 2FA is active:
    try:
        WebDriverWait(browser, 10).until(EC.url_matches('https://www.bestbuy.com/identity/signin'))
    except:
        WebDriverWait(browser, 10).until(EC.url_matches(BB_CHECKOUT_URL))
    else:
        is_signed_in = sign_in(browser, is_signed_in)
        if is_signed_in:
            print('Signed in successfully')
        else:
            print('Unable to sign in!')
    '''

    # Wait until browser load properly
    checkout_pg_wait(browser)

    # Switch to shipping option (if available)
    if shipping:
        try:
            browser.find_element_by_link_text(BB_SHIPPING_OPTION_LINKTEXT).click()
        except:
            print('Shipping already set or unable to select shipping option!\n')
            select_pickup_store(browser)
        else:
            print('Selected shipping option.\n')
    else:
        select_pickup_store(browser)

    checkout_pg_wait(browser)
    if payment_method_ready:
        # Credit Card CVV Code
        browser.find_element_by_id(BB_CREDIT_CVV_ID).send_keys(cvv_num)

    # Place order
    current_payment_url = browser.current_url
    for retry in range(3):
        try:
            checkout_pg_wait(browser)
            browser.find_element_by_css_selector(BB_PLACE_ORDER_CSS_SELECTOR).click()
        except:
            print('Unable to place the order!\n Retrying... \n')
        else:
            break

    try:
        WebDriverWait(browser, 20).until(EC.url_changes(current_payment_url))
    except:
        print_current_time()
        print('Credit card not valid! Please check payment option.')
        return False
    else:
        print_current_time()
        print('Success! Order has been placed.\n')
        return True

def select_pickup_store(browser):
    try:
        browser.find_element_by_css_selector(BB_CHANGE_PICKUP_STORE).click()
        WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.ID, BB_PICKUP_STORE_ID)))
        browser.find_element_by_css_selector(BB_PICKUP_STORE_CSS).click()
        browser.find_element_by_xpath(BB_SELECT_STORE_XPATH).click()
    except:
        print('Unable to select pickup store!')
    else:
        print('Selected chosen store')

def checkout_pg_wait(browser):
    WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, BB_PLACE_ORDER_CSS_SELECTOR)))


def NotifyOrderPlaced():
    pass
    '''
    title = '(BestBuy) Order has been automatically placed!'
    message = 'Congratulation! '+product_name+' is placed.'
    Notifier.notifyDesktop(title, message)
    Notifier.notifyPhoneEmail(title, message)
    '''

main()