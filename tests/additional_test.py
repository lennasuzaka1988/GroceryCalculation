import openpyxl
from openpyxl.drawing.image import Image
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl_image_loader import SheetImageLoader
import pandas as pd

from grocery_scraper import *
import import_grocery_list
from import_grocery_list import sprouts_grocery_list


grocery_list_xlsx = '../Grocery List.xlsx'
df_sprouts = pd.DataFrame(sprouts_grocery_list)


def first_item_search():
    product = import_grocery_list.df_sprouts.iat[0, 1]
    first_product_name_input(product)
    return closest_product_result(product)


def following_item_search():
    for row in import_grocery_list.df_sprouts['Item'].dropna()[1:]:
        clear_search()
        following_product_names_input(row)
        current_page = driver.current_url
        driver.get(current_page)
        time.sleep(10)
        bsoup = BeautifulSoup(driver.page_source, features='html5lib')
        print(bsoup.find('li').find_parent().get_text())


store_navigation('64154')
first_item_search()
time.sleep(10)
following_item_search()
