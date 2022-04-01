from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initializing the webdriver
options = webdriver.ChromeOptions()
options.add_argument('start-maximized')
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_argument('--disable-popup-blocking')
options.add_argument('--enable-javascript')
options.add_argument('--disable-notifications')
options.add_experimental_option('detach', True)

driver = webdriver.Chrome(options=options)


# Swapping to the appropriate store
def store_navigation():
    driver.get('https://www.sprouts.com/store/mo/kansas-city/kansas-city/')
    # Waiting for that damn popup
    clicking_maybe_later = WebDriverWait(driver, timeout=20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="pop-up-dismiss"]')),
    )
    clicking_maybe_later.click()

    # Swap to Kansas City store via Store's Specials buttons
    driver.find_element(By.CSS_SELECTOR, '.cell.divider.small-6 > button').click()


# Only for the first product since paths and JavaScript changes a little after
def first_search(product):
    time.sleep(3)
    driver.find_element(By.XPATH,
                        '//*[@id="menu-item-2557"]/div/unata-search-nav/div/form/input').send_keys(product +
                                                                                                   Keys.ENTER)
    current_page = driver.current_url
    # Automation for the search results page
    driver.get(current_page)
    time.sleep(8)
    driver.find_element(By.XPATH, '/html//button[@id="shopping-selector-parent-process-modal-close-click"]').click()
    driver.find_element(By.CSS_SELECTOR,
                        'sticky-react-header > div > div.css-q1n3l > div.css-c1jgn7 > form > div > input').clear()

def subsequent_search(product):
    time.sleep(3)
    driver.find_element(By.XPATH,
                        '//input[@class="css-4hd4ug active focus-visible"]').send_keys(product +
                                                                                       Keys.ENTER)
    current_page = driver.current_url
    driver.get(current_page)


# Initializing Beautiful Soup and scraping for the price
def scraping_price():
    time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html5lib')
    soup.prettify()
    price = soup.select(
        '#content > div > div.shop-layout > div.content-wrapper > div > div:nth-child(2) > ol > '
        'li:nth-child(1) > div > div.cell-content-wrapper > div.cell-prices.product-prices > '
        'div > div > react-product-price > div > div.css-0 > span:nth-child(2) > span:nth-child(1)')
    for i in price:
        return i.text
