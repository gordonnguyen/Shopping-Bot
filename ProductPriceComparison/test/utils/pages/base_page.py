'''
    Base Page class for Best Buy Bot
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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