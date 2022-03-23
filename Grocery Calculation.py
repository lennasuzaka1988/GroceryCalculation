import pandas as pd
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


try:
    grocery_list = pd.read_excel('G:/Sync/Shared Folder/Groceries and Takeout/Grocery List2.xlsx')
except FileNotFoundError:
    grocery_list = pd.read_excel('D:/Sync/Shared Folder/Groceries and Takeout/Grocery List2.xlsx')
df = pd.DataFrame(grocery_list)


def grocery_prices():
    total_cost_of_product = round(df['Price'] * df['Quantity'], 2)
    grocery_bill = pd.DataFrame.sum(total_cost_of_product)
    bill_after_tax = round(grocery_bill * 0.10 + grocery_bill, 2)
    bill_with_dollar_sign = '${:,.2f}'.format(bill_after_tax)
    return bill_with_dollar_sign


driver = webdriver.Chrome()
driver.get('https://www.hy-vee.com/aisles-online')
driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div/div/header/div[2]/div[2]/div/div[1]/div/form/div/input')\
    .send_keys('Ritz' + Keys.ENTER)
time.sleep(5)


response = requests.get(driver.current_url)
response.execute_script('return document.readyState').equals('complete')
hy_vee_data = response.text

print(hy_vee_data)
# soup = BeautifulSoup(hy_vee_data, 'html.parser')
# for selection in soup.select('#main > div > div:nth-child(2) > div:nth-child(2) > '
#                            'div:nth-child(2) > div:nth-child(2) > div > article > div > div:nth-child(2)'):
#     print(selection)



# Label Sprouts and Hy-Vee, if in Sprouts column, detect images from Sprouts store only. If in Hy-vee, detect images
# from Hy-Vee only
# def export_images()