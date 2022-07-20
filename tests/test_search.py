from grocery_scraper import *


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


def img_url_list():
    time.sleep(5)
    img_url = []
    img_url_stripped = []
    img_url.append(image_scrape())
    for img in img_url:
        url_split = url_image_parse(img)['path'].rsplit('format(jpg)/', 1)[1]
        img_url_stripped.append(url_split)
    return img_url_stripped


# Function is for first product ONLY since paths and JavaScript changes a little for the subsequent searches
def first_search(product):
    # Input product from Excel spreadsheet and automating search
    input_product = WebDriverWait(driver, timeout=30).until(
        EC.presence_of_element_located((By.XPATH,
                                        '//*[@id="menu-item-2557"]/div/unata-search-nav/div/form/input')))
    input_product.send_keys(product + Keys.ENTER)

    # Waiting for and closing the shopping options pop-up
    modal_close_out()

    # Don't you dare remove the redundant parentheses lest you want everything to go kaboom
    return (img_url_list(), closest_product_result(product, bsoup))


# Same as first_search function but targeting new elements from subsequent results
def subsequent_search(product):
    time.sleep(5)

    input_box = WebDriverWait(driver, timeout=30).until(EC.presence_of_element_located((
        By.XPATH, '//*[@id="sticky-react-header"]/div/div[2]/div[1]/form/div/input')))

    input_box.send_keys(product + Keys.ENTER)

    time.sleep(5)

    driver.quit()
    # DON'T REMOVE PARENTHESES DAMMIT
    return (img_url_list(), closest_product_result(product, bsoup))


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


store_navigation('64154')
first_search('Gala Apple')

