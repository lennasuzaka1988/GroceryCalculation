import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import requests
from selenium.webdriver.support.select import Select
import time


# try:
#     grocery_list = pd.read_excel('G:/Sync/Shared Folder/Groceries and Takeout/Grocery List2.xlsx')
# except FileNotFoundError:
#     grocery_list = pd.read_excel('D:/Sync/Shared Folder/Groceries and Takeout/Grocery List2.xlsx')
# df = pd.DataFrame(grocery_list)
#
#
# def grocery_prices():
#     total_cost_of_product = round(df['Price'] * df['Quantity'], 2)
#     grocery_bill = pd.DataFrame.sum(total_cost_of_product)
#     bill_after_tax = round(grocery_bill * 0.10 + grocery_bill, 2)
#     bill_with_dollar_sign = '${:,.2f}'.format(bill_after_tax)
#     return bill_with_dollar_sign


driver = webdriver.Chrome()
driver.get('https://www.sprouts.com/')
time.sleep(5)
search_box = driver.execute_script("document.querySelector('#menu-item-2623 > div').shadowRoot")
print(search_box)
# search_box.find_element(By.CSS_SELECTOR('div[aria-label="Search"]'))
# search_click.click()
    # \.send_keys('Ritz' + Keys.ENTER)




# Label Sprouts, if in Sprouts column, detect images from Sprouts store only