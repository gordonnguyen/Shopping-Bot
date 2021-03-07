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
import Notifier

# Configuration
shipping = True
express_mode = False # Ignore shipping option. Checkout ASAP
payment_method_ready = True
cvv_num = '1'
account_2fa = True


# BESTBUY PAGE URLS:
product_name = 'RTX 3060 Ti (BestBuy)'
product_url = 'https://www.bestbuy.com/site/nvidia-geforce-rtx-3060-ti-8gb-gddr6-pci-express-4-0-graphics-card-steel-and-black/6439402.p?skuId=6439402'
#product_url = 'https://www.bestbuy.com/site/dell-inspiron-15-6-inch-fhd-touch-laptop-amd-ryzen-5-12gb-ram-256-gb-ssd-1-tb-hdd-black/6438338.p?skuId=6438338'
#product_url = 'https://www.bestbuy.com/site/apple-watch-se-gps-40mm-silver-aluminum-case-with-white-sport-band-silver/6215915.p?skuId=6215915'
#product_url = 'https://www.bestbuy.com/site/pny-nvidia-geforce-gt-1030-2gb-gddr5-pci-express-3-0-graphics-card-black/5901353.p?skuId=5901353'
#product_url = 'https://www.bestbuy.com/site/wd-easystore-480gb-solid-state-drive-for-laptops/6411192.p?skuId=6411192'
#product_url = 'https://www.bestbuy.com/site/sony-wh-ch510-wireless-on-ear-headphones-black/6359775.p?skuId=6359775'


BB_HOME_URL = 'https://www.bestbuy.com/'
BB_SIGNIN_URL = 'https://www.bestbuy.com/identity/global/signin'
BB_CHECKOUT_URL = 'https://www.bestbuy.com/checkout/r/fast-track'
BB_PAYMENT_URL = 'https://www.bestbuy.com/checkout/r/payment'

# BESTBUY SELECTORS:
BB_PRICE_HTML_SELECTOR = ('#prcIsum', '#mm-saleDscPrc', '#prcIsum_bidPrice')
BB_NAME_HTML_SELECTOR = '#itemTitle'
BB_2FA_CONTINUE_XPATH = '/html/body/div[1]/div/section/main/div[2]/div[1]/div/div/div/form/div[3]/button'
BB_ADD_TO_CART_XPATH = '/html/body/div[3]/main/div[2]/div/div[1]/div[3]/div[2]/div/div[2]/div[1]/div/div/div/button'
BB_ADD_TO_CART_CSS = '.btn.btn-primary.btn-lg.btn-block.btn-leading-ficon.add-to-cart-button'
BB_CART_POPUP_XPATH = '/html/body/div[7]/div'
BB_CART_POPUP_CSS_SELECTOR = '#shop-attach-modal-80876233-modal > div > div:nth-child(1) > div > div > div > div > div.top-nav-container-v2 > div.success'

BB_CHECKOUT = "#cartApp > div.page-spinner.page-spinner--out > div.large-view.size-l > div > div.fluid-large-view > div.fluid-large-view__upper-container > section.fluid-large-view__sidebar > div > div > div.order-summary__checkout-buttons-container > div > div.checkout-buttons__checkout > button"
BB_SHIPPING_RADIO_XPATH = '//*[@id="cartApp"]/*div[2]/div[1]/div/div'
BB_SHIPPING_OPTION_XPATH = '//*[@id="checkoutApp"]/div[2]/div[1]/div[1]/main/div[2]/div[2]/form/section/div/div[1]/div/div/section/div[2]/div[2]/div[2]/div/div/a'
#'//*[@id="checkoutApp"]/div[2]/div[1]/div[1]/main/div[2]/div[2]/form/section/div/div[1]/div/div/section[1]/div[2]/div[2]/div[2]/div/div/a'
                           #//*[@id="checkoutApp"]/div[2]/div[1]/div[1]/main/div[2]/div[2]/form/section/div/div[1]/div/div/section/div[2]/div[2]/div[2]/div/div/a
BB_SHIPPING_OPTION_LINKTEXT = 'Switch to Shipping'
BB_SHIPPING_OPTION_CSS_SELECTOR = 'a.ispu-card__switch'
BB_SHIPPING_RADIO_CSS_SELECTOR = 'div.availability__entry.availability--unselected.availability--remove-z-index > div > div'
BB_CONTINUE_PAYMENT_XPATH = '//*[@id="checkoutApp"]/div[2]/div[1]/div[1]/main/div[2]/div[2]/form/section/div/div[2]/div/div/button'
                            #//*[@id="checkoutApp"]/div[2]/div[1]/div[1]/main/div[2]/div[2]/form/section/div/div[2]/div/div/button
BB_PLACE_ORDER_XPATH = '//*[@id="checkoutApp"]/div[2]/div[1]/div[1]/main/div[2]/div[3]/div/section/div[4]/button'
                       #//*[@id="checkoutApp"]/div[2]/div[1]/div[1]/main/div[2]/div[3]/div/section/div[4]/button
BB_PLACE_ORDER_CSS_SELECTOR = '.btn.btn-lg.btn-block.btn-primary'
BB_CREDIT_CVV_ID = 'credit-card-cvv'

def main():
    order_placed = False
    browser = launchBrowser()
    signed_in_status = signIn(browser)
    if signed_in_status:
        loopAddtoCart(browser)
        order_placed = checkout(browser)
        if order_placed:
            NotifyOrderPlaced()
        while True:
            pass
    else:
        print('Unable to sign in!')

def printCurrentDateTime():
    print(datetime.datetime.now().strftime('< %m/%d/%Y - %H:%M:%S >'))

def launchBrowser():
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "eager"
    options = Options()
    chrome_path = 'C:/Users/maixa/Documents/NguyenAnhClassWork/PracticeProjects/ProductPriceComparison/chromedriver.exe'
    options.add_experimental_option("detach", True)
    return webdriver.Chrome(executable_path=chrome_path, desired_capabilities=caps, options=options)

def signIn(browser):
    BB_email_selector = 'fld-e'
    BB_email = 'maixanh45@yahoo.com'
    BB_password_selector = 'fld-p1'
    BB_password = '@Maixanh45'
    BB_signin_selector = 'cia-form__controls '
    BB_verification_id_selector = 'verificationCode'
    ####
    browser.get(BB_SIGNIN_URL)
    current_signin_url = browser.current_url
    # Fill email and password fields
    browser.find_element_by_id(BB_email_selector).send_keys(BB_email)
    browser.find_element_by_id(BB_password_selector).send_keys(BB_password)
    
    # Submit / Signin button
    browser.find_element_by_class_name(BB_signin_selector).click()

    if account_2fa == True:
        try:
            # Wait for user to type 2fa code
            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, BB_verification_id_selector)))
            WebDriverWait(browser, 120).until_not(EC.presence_of_element_located((By.ID, BB_verification_id_selector)))
        except:
            return False
        else:
            print('Signed in successfully!\n')
            return True
    else:
        try:
            WebDriverWait(browser, 10).until(EC.url_changes(current_signin_url))
        except:
            print('Incorrect account name or password!\n')
            return False
        else:
            print('Signed in successfully!\n')
            return True

def loopAddtoCart(browser):
    browser.get(product_url)
    # Force redirect to product page if stuck
    while browser.current_url not in product_url:
        browser.get(product_url)

    # Add product to cart
    count = 0
    while True:
        try:
            WebDriverWait(browser, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, BB_ADD_TO_CART_CSS)))
            addtocart_btn = browser.find_element_by_css_selector(BB_ADD_TO_CART_CSS)
        except:
            count += 1
            if count == 1:
                print('Product currently unavailable! Refreshing page...\n')
            elif count%10 == 0:
                printCurrentDateTime()
                print('Still unavailable! Retries count:', count, '\n<Refreshing page again...>\n')
            browser.get(product_url)
        else:
            printCurrentDateTime()
            print('Product is available!!!\n')
            break

    addtocart_btn.click()
    print('Adding to cart...')
    add_to_cart_count = 1
    while True: 
        try:
            browser.find_element(By.CSS_SELECTOR, '.spinner.spinner-sm')
        except:
            addtocart_btn.click()
            if add_to_cart_count == 1:
                datetime.datetime.now().strftime("%m/%d/%Y, %H:%M%:S")
                print('Button stuck. Retrying!\n')
            add_to_cart_count = 0
        else:
            break

    WebDriverWait(browser, 20).until_not(EC.presence_of_element_located((By.CSS_SELECTOR, '.spinner.spinner-sm')))
    print('Product added to cart!')

def checkout(browser):
    browser.get(BB_CHECKOUT_URL)
    # Switch to shipping option (if available)
    if shipping:
        try:
            WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, BB_CONTINUE_PAYMENT_XPATH)))
            browser.find_element_by_link_text(BB_SHIPPING_OPTION_LINKTEXT).click()
        except:
            print('Shipping already set or unable to select shipping option!\n')
        else:
            print('Selected shipping option.\n')
    if payment_method_ready == False:
        try:
            WebDriverWait(browser, 30).until(EC.element_to_be_clickable((By.XPATH, BB_CONTINUE_PAYMENT_XPATH)))
            browser.find_element_by_xpath(BB_CONTINUE_PAYMENT_XPATH).click()
        except Error as err:
            print(err)
            print('Unable to continue to payment!\n')
        else:
            printCurrentDateTime
            print('Continuing to payment...')
    else:
        # Credit Card CVV Code
        browser.find_element_by_id(BB_CREDIT_CVV_ID).send_keys(cvv_num)

    # Place order
    for retry in range(3):
        try:
            WebDriverWait(browser, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, BB_PLACE_ORDER_CSS_SELECTOR)))
            browser.find_element_by_css_selector(BB_PLACE_ORDER_CSS_SELECTOR).click()
        except:
            print('Unable to place the order!\n Retrying... \n')
        else:
            break

    try:
        WebDriverWait(browser, 120).until(EC.url_changes(BB_PAYMENT_URL))
    except:
        print('Credit card not valid! Please check payment option.')
        return False
    else:
        print('Success! Order has been placed.\n')
        return True

def NotifyOrderPlaced():
    title = '(BestBuy) Order has been automatically placed!'
    message = 'Congratulation! '+product_name+' is placed.'
    Notifier.notifyDesktop(title, message)
    Notifier.notifyPhoneEmail(title, message)

main()