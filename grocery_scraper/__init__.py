from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.actions import pointer_actions
import random
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


# Clearing the search bar after every search for a product
def clear_search():
    time.sleep(5)
    input_element = driver.find_element(By.XPATH, '//*[@id="sticky-react-header"]/div/div[2]/div[1]/form/div/input')
    time.sleep(5)
    hover = ActionChains(driver).move_to_element(input_element).click().key_down(Keys.CONTROL) \
        .send_keys('a').key_up(Keys.CONTROL).send_keys(Keys.DELETE)
    hover.perform()


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


# Initializing Beautiful Soup and scraping for the price
def scraping_price():
    time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html5lib')
    soup.prettify()
    price = soup.select(
        'react-product-price:nth-child(1) > div > div > span:nth-child(1) > span:nth-child(1)')
    for i in price:
        return i.text


# Only for the first product since paths and JavaScript changes a little after
def first_search(product):
    time.sleep(5)
    driver.find_element(By.XPATH,
                        '//*[@id="menu-item-2557"]/div/unata-search-nav/div/form/input').send_keys(product +
                                                                                                   Keys.ENTER)
    current_page = driver.current_url

    # Automation for the search results page
    driver.get(current_page)
    time.sleep(8)
    driver.find_element(By.XPATH, '/html//button[@id="shopping-selector-parent-process-modal-close-click"]').click()
    time.sleep(5)
    expand_info = driver.find_element(By.CSS_SELECTOR, 'ol > li:nth-child(1) > div > div.cell-image-wrapper > span.cell-image.show')
    action = ActionChains(driver)
    action.move_to_element(expand_info).click().perform()
    time.sleep(5)
    driver.find_element(By.XPATH, '//div[1]/div/div/div/div/div[1]/button').click()
    time.sleep(3)
    clear_search()
    return scraping_price()


def subsequent_search(product):
    time.sleep(5)
    driver.find_element(By.XPATH,
                        '//*[@id="sticky-react-header"]/div/div[2]/div[1]/form/div/input').send_keys(product +
                                                                                                     Keys.ENTER)
    current_page = driver.current_url
    time.sleep(3)
    driver.get(current_page)
    time.sleep(4)
    expand_info = driver.find_element(By.CSS_SELECTOR, 'ol > li:nth-child(1) > div > div.cell-image-wrapper > span.cell-image.show')
    action = ActionChains(driver)
    action.move_to_element(expand_info).click().perform()
    time.sleep(5)
    driver.find_element(By.XPATH, '//div[1]/div/div/div/div/div[1]/button').click()
    time.sleep(3)
    clear_search()
    return scraping_price()
