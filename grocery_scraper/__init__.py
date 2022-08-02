from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse
import time
import re

# Initializing the webdriver
webdriver.Chrome(service=Service(ChromeDriverManager().install()))
options = webdriver.ChromeOptions()
options.add_argument('start-maximized')
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_argument('--disable-popup-blocking')
options.add_argument('--enable-javascript')
options.add_argument('--disable-notifications')
options.add_experimental_option('detach', True)
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)


# Clearing the search bar after every search for a product
def clear_search_and_input():
    input_element_wait = wait.until(EC.presence_of_element_located((
        By.XPATH, '//*[@id="sticky-react-header"]/div/div[2]/div[1]/form/div/input')))
    hover = ActionChains(driver).move_to_element(input_element_wait).click().key_down(Keys.CONTROL) \
        .send_keys('a').key_up(Keys.CONTROL).send_keys(Keys.DELETE)
    hover.perform()


def modal_close_out():
    time.sleep(5)
    shopping_selector_wait = WebDriverWait(driver, timeout=30).until(EC.visibility_of_element_located((
        By.XPATH, '/html//button[@id="shopping-selector-parent-process-modal-close-click"]')))
    shopping_selector_wait.click()
    time.sleep(5)


# Changes location of store, by doing the following: go to store selector link and click on it >
# enter zip code > click the closest store to the entered zip code
def store_navigation(zip_code):
    driver.get('https://www.sprouts.com/weekly-ad/')
    store_selector_button = WebDriverWait(driver, timeout=20).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR,
             '#secondary-navigation > div > ul > li:nth-child(1) > div > '
             'unata-unified-header > div > div:nth-child(2) > span > unata-storeid-label > '
             'a')))
    store_selector_button.click()
    zip_code_input_box = WebDriverWait(driver, timeout=10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,
                                    'unata-root > dialog-holder > dialog-wrapper > div > unata-store-selector '
                                    '> div > div > div:nth-child(2) > div > div > unata-store-map-mapbox > '
                                    'div > div:nth-child(1) > div > div:nth-child(2) > form > div > input')))
    zip_code_input_box.click()
    zip_code_input_box.send_keys(zip_code + Keys.ENTER)
    click_store_select_button = WebDriverWait(driver, timeout=10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,
                                    'unata-root > dialog-holder > dialog-wrapper > div > unata-store-selector > '
                                    'div > div > div:nth-child(2) > div > div > unata-store-map-mapbox > div > '
                                    'div:nth-child(2) > div > div > div > ol > li:nth-child(1) > table > tbody > tr > '
                                    'td:nth-child(2) > button')))
    click_store_select_button.click()
    time.sleep(5)


def stripping_beautiful_soup_extraction_text(string):
    reg = re.compile(r'\s.[a-z]+')
    strip_context = reg.sub('', string)
    return strip_context


# Initializing BeautifulSoup to scrape for price
def closest_product_result(product_name, soup):
    product_input_list = []
    product_input_price_list = []
    # img_url_stripped = []
    product_input = soup.find('ol').find(string=re.compile(product_name))
    product_input_list.append(product_input)
    # try:
    #     price_text = product_input.find_parent().find_parent().find_parent().find_previous_sibling().get_text()
    # except AttributeError:
    #     price_text = product_input.find_parent().find_parent()
    # product_input_price_list.append(stripping_beautiful_soup_extraction_text(price_text))
    # direct_to_img = product_input.find_parent().find_parent().find_parent().find_parent().find_previous_sibling().find('img')['src']
    # stripped_img_url = url_image_parse(direct_to_img)['path'].rsplit('format(jpg)/', 1)[1]
    # img_url_stripped.append(stripped_img_url)
    # return (product_input_price_list, img_url_stripped)
    return (product_input_list, product_input_price_list)


# Stripping down the url in order to access the image
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


# Function is for first product ONLY since paths and JavaScript changes a little for the subsequent searches
def first_product_name_input(product):
    # Input product from Excel spreadsheet and automating search
    input_product = WebDriverWait(driver, timeout=30).until(
        EC.presence_of_element_located((By.XPATH,
                                        '//*[@id="menu-item-2557"]/div/unata-search-nav/div/form/input')))
    input_product.send_keys(product + Keys.ENTER)

    # Waiting for and closing the shopping options pop-up
    modal_close_out()
    time.sleep(10)


def following_product_names_input(following_product):
    try:
        input_box = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="sticky-react-header"]/div/div[2]/div[1]/form/div/input')))
        input_box.send_keys(following_product + Keys.ENTER)
    except TimeoutException:
        print('Timed out waiting for page to load')


def product_info_list_output(product_name):
    first_product_name_input(product_name)
    url = driver.current_url
    wait.until(EC.url_to_be(url))
    page_source = driver.page_source
    page_soup = BeautifulSoup(page_source, 'html.parser')
    page_soup.prettify()
    first_result = closest_product_result(product_name, page_soup)
    clear_search_and_input()
    return first_result


store_navigation('64154')
print(product_info_list_output('Gala Apple'))
