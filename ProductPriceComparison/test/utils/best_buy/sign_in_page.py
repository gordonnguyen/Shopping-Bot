from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from utils.best_buy.base_page import BasePage
from utils.best_buy.locators import SignInPageLocators
from utils.best_buy.urls import MainUrls


class SignInPage(BasePage):
    '''
        This object is a subclass of SignInPage(BasePage)
        specialized on BestBuy website
    '''
    BB_email_selector = 'fld-e'
    BB_password_selector = 'fld-p1'
    BB_signin_selector = 'cia-form__controls '  # Used for 2fa continue
    BB_verify_field_ID = 'verificationCode'
    BB_2fa_text_option_ID = 'sms-radio'
    BB_2fa_text_option_XPATH = '/html/body/div[1]/div/section/main/div[2]/div[1]/div/div/div/div/form/fieldset/fieldset/div[3]/label/div/i'
    BB_2fa_email_option_ID = 'email-radio'
    BB_sms_4digits_ID = 'smsDigits'

    # This function initilize email, password and sms_digits
    def __init__(self, driver):
        super().__init__(driver)
        self.url = MainUrls.sign_in
        self.email = 'maixanh45@yahoo.com'
        self.password = '@Nhan021400'
        self.sms_digits = '9386'

    def sign_in(self):
        # Fill email and password fields
        self.enter_text(SignInPageLocators.email_fld, self.email)
        self.enter_text(SignInPageLocators.password_fld, self.password)

        # Submit / Signin button
        self.driver.find_element_by_class_name(self.BB_signin_selector).click()
        self.wait.until(EC.url_changes(self.driver.current_url))
        #WebDriverWait(driver, 10).until(EC.url_changes(current_signin_url))

    # This function check if the current page is for verifying two factor authentication (2FA)
    def is_2fa(self):
        current_url = self.driver.current_url
        print('Current 2FA url: ', current_url)
        try:
            # Check if an option for sms verification method is available
            self.sms_opt_btn = self.wait.until(EC.element_to_be_clickable(SignInPageLocators.f2a_text_option))
        except:
            return False
        else:
            print('SMS FLD DETECTED')
            return True

    # This function enter email or phone, where website will then send a 2FA Code to.
    def prefill_2fa(self):
        # Select and Enter sms digits
        print('Require user interaction!')
        #driver.find_element_by_xpath(self.BB_2fa_text_option_XPATH).click()
        self.sms_opt_btn.click()
        self.wait.until(EC.element_to_be_clickable(SignInPageLocators.sms_digits_fld)).send_keys(self.sms_digits)
        #self.driver.find_element_by_id(SignInPageLocators.sms_digits_fld).send_keys(self.sms_digits)
        self.driver.find_element(*SignInPageLocators.signin_btn).click()

        # Wait for user to type 2fa code
        self.wait.until(EC.presence_of_element_located(SignInPageLocators.verify_code_fld))
        WebDriverWait(self.driver, 240).until_not(EC.presence_of_element_located(SignInPageLocators.verify_code_fld))
    
