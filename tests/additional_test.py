from bs4 import BeautifulSoup
import openpyxl
from openpyxl.drawing.image import Image
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl_image_loader import SheetImageLoader
import pandas as pd
import re


from grocery_scraper import *
import import_grocery_list
from import_grocery_list import sprouts_grocery_list


grocery_list_xlsx = '../Grocery List.xlsx'
df_sprouts = pd.DataFrame(sprouts_grocery_list)
sprouts_items = pd.DataFrame(sprouts_grocery_list, columns=['Item', 'Price'])


def first_item_search():
    product = import_grocery_list.df_sprouts.iat[0, 1]
    first_product_name_input(product)
    return closest_product_result(product)


def following_item_search():
    for index, row in sprouts_items.items():
        for x in row.dropna()[1:]:
            clear_search()
            following_product_names_input(x)
            time.sleep(10)
            current_page = driver.current_url
            driver.get(current_page)
            result = driver.find_element(By.XPATH, '//div[text()="%s"]' % x)
            print(result)
            # time.sleep(5)
            # bsoup = BeautifulSoup(driver.page_source, features='html5lib')
            # bsoup.prettify()
            # for product in bsoup.find_all(x):
            #     return product


store_navigation('64154')
first_item_search()
following_item_search()
driver.quit()
