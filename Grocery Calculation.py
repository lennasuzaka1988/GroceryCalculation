import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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


options = webdriver.ChromeOptions()
options.add_argument('start-maximized')
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_argument('--enable-javascript')
options.add_experimental_option('detach', True)
driver = webdriver.Chrome(options=options)

wait = WebDriverWait(driver, 10)

driver.get('https://www.sprouts.com/')
driver.find_element(By.XPATH, "//ul[@id='ubermenu-nav-main-4-top-bar-r']//div[@role='button']").click()



# Label Sprouts, if in Sprouts column, detect images from Sprouts store only