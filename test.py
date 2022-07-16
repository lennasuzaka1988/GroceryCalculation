from bs4 import BeautifulSoup
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


product_name = 'Gala Apple'


def closest_product_result():
    product_input_list = []
    product_input_price_list = []
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    soup.prettify()
    product_input = soup.find(string=re.compile(product_name))
    product_input_list.append(product_input)
    product_input_price_list.append(product_input.find_parent().find_parent().find('div', class_='css-1kh7mkb').text.strip('/lb'))
    print(product_input_list)
    print(product_input_price_list)
    # product_input.select_one('h2:has(span[@css-23422]) + ul')


# Find the price next to product input
modal_close_out()
time.sleep(5)
closest_product_result()
driver.quit()
