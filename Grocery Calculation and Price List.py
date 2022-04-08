import pandas as pd
from grocery_scraper import *
from ExcelGroceryFormat import *


# A simple grocery calculator for the weekly grocery list
try:
    grocery_list = pd.read_excel('G:/Sync/Shared Folder/Groceries and Takeout/Grocery List.xlsx')
except FileNotFoundError:
    grocery_list = pd.read_excel('D:/Sync/Shared Folder/Groceries and Takeout/Grocery List.xlsx')
df = pd.DataFrame(grocery_list)


def grocery_prices():
    total_cost_of_product = round(df['Price'] * df['Quantity'], 2)
    grocery_bill = pd.DataFrame.sum(total_cost_of_product)
    bill_after_tax = round(grocery_bill * 0.10 + grocery_bill, 2)
    bill_with_dollar_sign = '${:,.2f}'.format(bill_after_tax)
    return bill_with_dollar_sign


#### AUTOMATED PRICE SCRAPING BELOW ####

scraped_prices = []
df_scraped_prices = pd.DataFrame(scraped_prices)


# Navigating to local store's search page
store_navigation()


# Searching for first product (requires separate function because of changed HTML in first product's results page)
def first_product_search():
    first_product = df.iat[1, 1]
    scraped_prices.append(first_search(first_product))


first_product_search()


for row in df['Item'].dropna()[1:]:
    scraped_prices.append((subsequent_search(row)))

print(scraped_prices)


# Replacing prices in Grocery List workbook with newly scraped prices
# grocery_list_xlsx = 'Grocery List.xlsx'
# workbook = load_workbook(grocery_list_xlsx)
# worksheet = workbook['Sprouts']


# worksheet.cell(row=1, column=3)



# for index, value in enumerate(scraped_prices, start=1):
#     worksheet.cell(row=index + 2, column=3, value=value)
#
#
# for row in worksheet['C']:
#     row.number_format = '$0.00'
# workbook.save(filename=grocery_list_xlsx)



# Please refer to Excel Grocery Format.py for Python-based formatting and inclusion of images




