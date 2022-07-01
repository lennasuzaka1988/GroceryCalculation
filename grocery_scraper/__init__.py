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
    input_element_wait = WebDriverWait(driver, timeout=10).until(EC.presence_of_element_located((
        By.XPATH, '//*[@id="sticky-react-header"]/div/div[2]/div[1]/form/div/input')))
    hover = ActionChains(driver).move_to_element(input_element_wait).click().key_down(Keys.CONTROL) \
        .send_keys('a').key_up(Keys.CONTROL).send_keys(Keys.DELETE)
    hover.perform()


# The unnecessarily long process to change the location
def store_navigation(zip_code):
    driver.get('https://www.sprouts.com/weekly-ad/')
    store_selector = WebDriverWait(driver, timeout=10).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR,
             '#secondary-navigation > div > ul > li:nth-child(1) > div > '
             'unata-unified-header > div > div:nth-child(2) > span > unata-storeid-label > '
             'a')))
    store_selector.click()
    zip_code_input = WebDriverWait(driver, timeout=10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,
                                    'unata-root > dialog-holder > dialog-wrapper > div > unata-store-selector '
                                    '> div > div > div:nth-child(2) > div > div > unata-store-map-mapbox > '
                                    'div > div:nth-child(1) > div > div:nth-child(2) > form > div > input')))
    zip_code_input.click()
    zip_code_input.send_keys(zip_code + Keys.ENTER)
    click_select_button = WebDriverWait(driver, timeout=10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,
                                    'unata-root > dialog-holder > dialog-wrapper > div > unata-store-selector > '
                                    'div > div > div:nth-child(2) > div > div > unata-store-map-mapbox > div > '
                                    'div:nth-child(2) > div > div > div > ol > li:nth-child(1) > table > tbody > tr > '
                                    'td:nth-child(2) > button')))
    click_select_button.click()


# Initializing BeautifulSoup to scrape for price
def scraping_price():
    clear_search()
    time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html5lib')
    soup.prettify()
    if soup.select('li:nth-child(1) > div > react-item-tile > div > div > div:nth-child(3) > div:nth-child(1) > span:nth-child(1)'):
        for i in soup.select('li:nth-child(1) > div > react-item-tile > div > div > div:nth-child(3) > div:nth-child(1) > span:nth-child(1)'):
            return i.text.rsplit(' /ea', 1)[0]
    else:
        price_2 = soup.select(
            'react-product-price:nth-child(1) > div > div:nth-child(2) > span:nth-child(1) > span:nth-child(1)'
        )
        for two in price_2:
            return two.text.rsplit(' /ea', 1)[0]


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
def first_search(product):
    first_price = []
    first_image_url = []
    image_url_stripped = []

    # Input product from Excel spreadsheet and automating search
    input_product = WebDriverWait(driver, timeout=30).until(
        EC.presence_of_element_located((By.XPATH,
                                        '//*[@id="menu-item-2557"]/div/unata-search-nav/div/form/input')))
    input_product.send_keys(product + Keys.ENTER)

    # Waiting for and closing the shopping options pop-up
    time.sleep(5)
    shopping_selector_wait = WebDriverWait(driver, timeout=90).until(EC.visibility_of_element_located((
        By.XPATH, '/html//button[@id="shopping-selector-parent-process-modal-close-click"]')))
    shopping_selector_wait.click()

    # Scraping for the image
    time.sleep(5)
    first_image_url.append(image_scrape())

    for img in first_image_url:
        url_split = url_image_parse(img)['path'].rsplit('format(jpg)/', 1)[1]
        image_url_stripped.append(url_split)
    first_price.append(scraping_price())

    # Don't you dare remove the redundant parentheses lest you want everything to go kaboom
    return (first_price, image_url_stripped)


def subsequent_search(product):
    prices = []
    image_url = []
    img_url_stripped = []
    time.sleep(5)
    # Same as first_search function but targeting new elements from subsequent results
    input_box = WebDriverWait(driver, timeout=30).until(EC.presence_of_element_located((
        By.XPATH, '//*[@id="sticky-react-header"]/div/div[2]/div[1]/form/div/input')))

    input_box.send_keys(product + Keys.ENTER)

    current_page = driver.current_url
    driver.get(current_page)

    time.sleep(5)
    image_url.append(image_scrape())

    for img in image_url:
        url_img_split = url_image_parse(img)['path'].rsplit('format(jpg)/', 1)[1]
        img_url_stripped.append(url_img_split)
    prices.append(scraping_price())

    driver.quit()
    # DON'T REMOVE PARENTHESES DAMMIT
    return (prices, img_url_stripped)


def image_scrape():
    time.sleep(5)
    try:
        return WebDriverWait(driver, timeout=30).until(EC.presence_of_element_located((By.XPATH,
                                                                                       '//*[@id="content"]/div/div[2]/div[2]/div/div[2]/ol/li[1]/div/react-item-tile/div/div/div[2]/button/div/div/span/img'))).get_attribute(
            'src')
    except TimeoutException:
        return WebDriverWait(driver, timeout=30).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                       'main > div > div:nth-child(2) > div:nth-child(2) > div > div:nth-child(2) > ol > li:nth-child(1) > div > div:nth-child(3) > span'))).get_attribute(
            'data-src')
