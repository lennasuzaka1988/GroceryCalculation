import itertools
import urllib
import urllib.request

import openpyxl
import pandas as pd
from openpyxl.drawing.image import Image
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl_image_loader import SheetImageLoader

from grocery_scraper import *
import import_grocery_list

# Have to separate Sprouts and Hy-Vee lists into different spreadsheets as scraping only applies to Sprouts
# (Hy-Vee disallows scraping), info pulled from import_grocery_list module
grocery_list_xlsx = '../Grocery List.xlsx'
all_prices_and_images = []


def price_and_image_scraping():
    wb = openpyxl.load_workbook(grocery_list_xlsx)
    ws_sprouts = wb['Sprouts']
    rows = dataframe_to_rows(product_df, index=False, header=False)

    # Apply value to cell if no value is listed
    for row_index, row in enumerate(rows, 2):
        for column_index, value in enumerate(row, 3):
            if ws_sprouts.cell(row=row_index, column=column_index).value and column_index == 3:
                pass
            else:
                ws_sprouts.cell(row=row_index, column=column_index, value=value)
    wb.save(grocery_list_xlsx)


# Need to convert results from all_prices_and_images() to dataframe for scraping output
product_df = pd.DataFrame(all_prices_and_images, columns=['Price', 'Image'])


def attach_excel_images():
    workbk = openpyxl.load_workbook(grocery_list_xlsx)
    ws_sprouts = workbk['Sprouts']
    image_loader = SheetImageLoader(ws_sprouts)

    img_urls = []
    cell_coordinates = []

    for image_row in ws_sprouts.iter_rows(min_row=2, min_col=4, max_col=4):
        for cell in image_row:
            img_urls.append(str(cell.value))
            cell_coordinates.append('F' + str(cell.row))

    file_names = []

    count = 1
    for i in img_urls:
        urllib.request.urlretrieve(i, f'image_0{str(count)}.png')
        file_names.append(f'image_0{str(count)}.png')
        count += 1

    file_dict = dict(zip(file_names, cell_coordinates))

    for file, location in file_dict.items():
        if image_loader.image_in(location):
            print('Image already exists!')
        else:
            img = Image(file)
            img.height = 65
            img.width = 65
            img.anchor = location
            ws_sprouts.add_image(img)
    workbk.save(grocery_list_xlsx)


# Searching for first product (requires separate function because of changed HTML in first product's results page) and
# subsequent products
def first_product_search():
    first_product = import_grocery_list.df_sprouts.iat[0, 1]
    first_product_result = first_search(first_product)
    all_prices_and_images.append(list(itertools.chain(*first_product_result)))
    # price_and_image_scraping()
    # attach_excel_images()
    # return first_product_result


def following_product_searches():
    for row in import_grocery_list.df_sprouts['Item'].dropna()[1:]:
        list_2_results = list(subsequent_search(row))
        all_prices_and_images.append(list(itertools.chain(*list_2_results)))
#         price_and_image_scraping()
#         attach_excel_images()


store_navigation('64154')
time.sleep(5)
first_product_search()
following_product_searches()
print(all_prices_and_images)

# develop accuracy changes
# develop way to wipe out columns
