from bs4 import BeautifulSoup, BeautifulStoneSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse
import time
import re

options = webdriver.ChromeOptions()
options.add_argument('start-maximized')
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_argument('--disable-popup-blocking')
options.add_argument('--enable-javascript')
options.add_argument('--disable-notifications')
options.add_experimental_option('detach', True)
driver = webdriver.Chrome(options=options)

driver.get('https://shop.sprouts.com/search?search_term=apple')


def modal_close_out():
    time.sleep(5)
    shopping_selector_wait = WebDriverWait(driver, timeout=30).until(EC.visibility_of_element_located((
        By.XPATH, '/html//button[@id="shopping-selector-parent-process-modal-close-click"]')))
    shopping_selector_wait.click()
    time.sleep(5)


def stripping_text(string):
    reg = re.compile(r'\s.[a-z]+')
    strip_context = reg.sub('', string)
    return strip_context


def closest_product_result(product_name, soup):
    product_input_list = []
    product_input_price_list = []
    product_input = soup.find(string=re.compile(product_name))
    price_text = product_input.find_parent().find_parent().find_previous_sibling().get_text()
    product_input_list.append(product_input)
    product_input_price_list.append(stripping_text(price_text))
    return (product_input_list, product_input_price_list)


modal_close_out()
time.sleep(5)
bsoup = BeautifulSoup(driver.page_source, 'html.parser')
bsoup.prettify()
print(closest_product_result('Gala Apple', bsoup))
