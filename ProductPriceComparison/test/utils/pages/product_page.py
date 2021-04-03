'''
    Product Page
'''


from base_page import BasePage

class ProductPage(BasePage):
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
    '''
    def prod_page_check_add_cart(self):
        self.driver.get(self.url)

        # Check product is available
        addtocart_btn = prod_avail(driver)

        is_added_to_cart = try_add_to_cart(addtocart_btn, driver)
        if is_added_to_cart:
            print('Product added to cart!')
        else:
            print('Failed to add to cart')
    '''

    # __init__ Initialize and change current url to product url
    def __init__(self, driver, product_url):
        super().__init__(driver)
        self.prod_url = product_url
        if self.driver.current_url != self.prod_url:
            self.driver.get(self.prod_url)
        else:
            print('Already in product page')

    # this function click add to cart btn
    def add_to_cart(self):
        add_to_cart_count = 1
        add_cart_btn = self.get_add_cart_btn(self)
        
        if add_to_cart_count == 1:
            print('Adding to cart...')

        try: 
            add_cart_btn.click()
            WebDriverWait(self.driver, 0.25).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.spinner.spinner-sm')))
        except:
            if add_to_cart_count == 1:
                print_current_time()
                print('Button stuck. Retrying!\n')
            add_to_cart_count = 0
            return False
        else:
            WebDriverWait(self.driver, 10).until_not(EC.presence_of_element_located((By.CSS_SELECTOR, '.spinner.spinner-sm')))
            try:
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, self.BB_CART_POPUP_CSS_SELECTOR)))
            except:
                if EC.presence_of_element_located((By.CSS_SELECTOR, self.BB_CART_FAILED_CSS)):
                    print_current_time
                    print('Failed to add to cart. Retrying!!!\n')
                    time.sleep(4)
                return False
            else:
                return True

    # This function check the product availibility (return True if avail)
    def check_avail(self):
        avail_count = 0
        try:
            self.get_add_cart_btn(self)
            #addtocart_btn = driver.find_element_by_css_selector(bb_add_to_cart_css)
        except:
            return False
            
        else:
            return True
            
    def get_add_cart_btn(self):
        return WebDriverWait(self.driver, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, self.bb_add_to_cart_css)))