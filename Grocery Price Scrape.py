from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def driver():
    # Initializing the webdriver with options
    options = webdriver.ChromeOptions()
    options.add_argument('start-maximized')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--enable-javascript')
    options.add_argument('--disable-notifications')
    options.add_experimental_option('detach', True)
    return webdriver.Chrome(options=options)


def store_navigation():
    driver().get('https://www.sprouts.com/store/mo/kansas-city/kansas-city/')
    # Waiting for that damn popup
    clicking_maybe_later = WebDriverWait(driver(), timeout=20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="pop-up-dismiss"]')),
    )
    clicking_maybe_later.click()

    # Swap to Kansas City store via Store's Specials buttons
    return driver().find_element(By.CSS_SELECTOR, '.cell.divider.small-6 > button').click()


def search():
    time.sleep(3)
    driver().find_element(By.XPATH,
                          '//*[@id="menu-item-2557"]/div/unata-search-nav/div/form/input').send_keys('corn' +
                                                                                                     Keys.ENTER)
    current_page = driver().current_url
    # Automation for the search results page
    driver().get(current_page)
    time.sleep(8)
    return driver().find_element(By.XPATH, '/html//button[@id="shopping-selector-parent-process-modal-close-click"]').click()


# Initializing Beautiful Soup and scraping for the price
def scraping_price():
    time.sleep(5)
    html = driver().page_source
    soup = BeautifulSoup(html, 'html5lib')
    soup.prettify()
    price = soup.select('#content > div > div.shop-layout > div.content-wrapper > div > div:nth-child(2) > ol > li:nth-child(1) > div > div.cell-content-wrapper > div.cell-prices.product-prices > div > div > react-product-price > div > div.css-0 > span:nth-child(1) > span:nth-child(1)')
    for i in price:
        return i.text
