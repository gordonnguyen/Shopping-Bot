'''
    Super classes for Page object
    Serve as a base template for page 
    automating functions with selenium
'''
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage():
    
    # Initialize browser
    def __init__(self, driver):
        self.driver = driver

        # Wait for browser (10 seconds as default wait time)
        self.wait = WebDriverWait(driver, 10)


    # Wait for element to be clickable and click
    def click(self, by_locator):
        self.wait.until(EC.element_to_be_clickable(by_locator)).click()

    def set_url(self, url):
        self.url = url

    # Select element in webpage and fill text
    def enter_text(self, by_locator, text):
        self.wait.until(EC.visibility_of_element_located(by_locator)).send_keys(text)

    # Check if the current url is correct to use for this object
    def is_correct_url(self):
        print('Target url:', self.main_url)
        print('Current url:', self.driver.current_url)
        try:
            WebDriverWait(self.driver, 6).until(EC.url_to_be(self.main_url))
        except:
            print('Failed to detect url')
            return False
        else:
            print('Correct url')
            return True
        #if self.driver.current_url == self.main_url:

    def to_main_url(self):
        self.driver.get(self.url)

