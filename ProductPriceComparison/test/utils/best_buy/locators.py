'''
    Selectors are used for webdriver to locate elements within a webpage
'''
from selenium.webdriver.common.by import By

class Locators:
    ''' BESTBUY SELECTORS '''
    class ProductPage:
        # PRODUCT PAGE:
        #PRICE_HTML_SELECTOR = ('#prcIsum', '#mm-saleDscPrc', '#prcIsum_bidPrice')
        #NAME_HTML_SELECTOR = '#itemTitle'

        F2A_CONTINUE_XPATH = '/html/body/div[1]/div/section/main/div[2]/div[1]/div/div/div/form/div[3]/button'
        #BB_ADD_TO_CART_XPATH = '/html/body/div[3]/main/div[2]/div/div[1]/div[3]/div[2]/div/div[2]/div[1]/div/div/div/button'
        add_btn_animation = (By.CSS_SELECTOR,'.spinner.spinner-sm')
        add_cart_btn = (By.CSS_SELECTOR, '.btn.btn-primary.btn-lg.btn-block.btn-leading-ficon.add-to-cart-button')
        #BB_CART_POPUP_XPATH = '/html/body/div[7]/div'
        cart_popup = (By.CSS_SELECTOR,'span.added-to-cart')
        cart_failed_popup = (By.CSS_SELECTOR, 'div > div > div.c-alert-content')

    class CartPage:
        # CART PAGE:
        BB_TO_CHECKOUT_BTN_CSS = 'div.checkout-buttons__checkout > button'

    class CheckOutPage:
        # CHECKOUT PAGE:
        checkout = "#cartApp > div.page-spinner.page-spinner--out > div.large-view.size-l > div > div.fluid-large-view > div.fluid-large-view__upper-container > section.fluid-large-view__sidebar > div > div > div.order-summary__checkout-buttons-container > div > div.checkout-buttons__checkout > button"
        SHIPPING_RADIO_XPATH = '//*[@id="cartApp"]/*div[2]/div[1]/div/div'
        SHIPPING_OPTION_XPATH = '//*[@id="checkoutApp"]/div[2]/div[1]/div[1]/main/div[2]/div[2]/form/section/div/div[1]/div/div/section/div[2]/div[2]/div[2]/div/div/a'

        SHIPPING_OPTION_LINKTEXT = 'Switch to Shipping'
        SHIPPING_OPTION_CSS_SELECTOR = 'a.ispu-card__switch'
        SHIPPING_RADIO_CSS_SELECTOR = 'div.availability__entry.availability--unselected.availability--remove-z-index > div > div'
        CONTINUE_PAYMENT_XPATH = '//*[@id="checkoutApp"]/div[2]/div[1]/div[1]/main/div[2]/div[2]/form/section/div/div[2]/div/div/button'

        PLACE_ORDER_XPATH = '//*[@id="checkoutApp"]/div[2]/div[1]/div[1]/main/div[2]/div[3]/div/section/div[4]/button'

        PLACE_ORDER_CSS_SELECTOR = '.btn.btn-lg.btn-block.btn-primary'
        CREDIT_CVV_ID = 'credit-card-cvv'

        CHANGE_PICKUP_STORE = 'a.btn-default-link.link-styled-button.ispu-display__change'
        PICKUP_STORE_ID = 'store-213-fulfillment'        # Sharptown 8210 S Gessner Dr Houston, TX 77036
        PICKUP_STORE_CSS = '#store-213-fulfillment-wrapper > a'
        SELECT_STORE_XPATH = '//*[@id="sc-store-availability-modal"]/div/div/div[2]/div/div/div[2]/div[3]/div[3]/div'