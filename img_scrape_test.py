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


def url_image_parse(img):
    image_parser = urlparse(img)
    elements = {
        'scheme': image_parser.scheme,
        'netloc': image_parser.netloc,
        'path': image_parser.path,
        'params': image_parser.params,
        'query': image_parser.query,
        'fragment': image_parser.fragment
    }
    return elements


def modal_close_out():
    time.sleep(5)
    shopping_selector_wait = WebDriverWait(driver, timeout=30).until(EC.visibility_of_element_located((
        By.XPATH, '/html//button[@id="shopping-selector-parent-process-modal-close-click"]')))
    shopping_selector_wait.click()
    time.sleep(5)


def product_image_scrape():
    first_image_url = []
    image_url_stripped = []
    first_image_url.append(image_scrape())
    for img in first_image_url:
        url_split = url_image_parse(img)['path'].rsplit('format(jpg)/', 1)[1]
        image_url_stripped.append(url_split)
    return image_url_stripped


def image_scrape():
    time.sleep(5)
    try:
        return WebDriverWait(driver, timeout=30).until(EC.presence_of_element_located((By.XPATH,
                                                                                       '//*[@id="content"]/div/div[2]/div[2]/div/div[2]/ol/li[1]/div/react-item-tile/div/div/div[2]/button/div/div/span/img'))).get_attribute('src')
    except TimeoutException:
        return WebDriverWait(driver, timeout=30).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                       'main > div > div:nth-child(2) > div:nth-child(2) > div > div:nth-child(2) > ol > li:nth-child(1) > div > div:nth-child(3) > span'))).get_attribute('data-src')


modal_close_out()
print(image_scrape())
print(product_image_scrape())
