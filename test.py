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
    product_list = []
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    soup.prettify()
    for ol in soup.find_all('div', class_='css-f85de'):
        for elem in ol(string=re.compile(product_name)):
            product_list.append(elem.text)
    print(product_list)


def closest_product_price_scrape():
    product_soup = BeautifulSoup(driver.page_source, 'html.parser')
    product_soup.prettify()
    ol = product_soup.find('ol')
    for li in ol.children:
        return li


modal_close_out()
print(closest_product_result())
time.sleep(10)
driver.quit()
