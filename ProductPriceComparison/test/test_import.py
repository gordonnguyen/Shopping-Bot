
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import utils.best_buy
from utils.best_buy import urls
from utils.best_buy.locators import Locators
from utils.best_buy.product_page import ProductPage