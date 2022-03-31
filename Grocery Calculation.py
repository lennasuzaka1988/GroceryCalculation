import pandas as pd
# from grocery_scraper import *

try:
    # grocery_list = pd.read_excel('G:/Sync/Shared Folder/Groceries and Takeout/Grocery List.xlsx')
    grocery_list = pd.read_excel('Grocery List.xlsx')
except FileNotFoundError:
    grocery_list = pd.read_excel('D:/Sync/Shared Folder/Groceries and Takeout/Grocery List.xlsx')
df = pd.DataFrame(grocery_list)


def grocery_prices():
    total_cost_of_product = round(df['Price'] * df['Quantity'], 2)
    grocery_bill = pd.DataFrame.sum(total_cost_of_product)
    bill_after_tax = round(grocery_bill * 0.10 + grocery_bill, 2)
    bill_with_dollar_sign = '${:,.2f}'.format(bill_after_tax)
    return bill_with_dollar_sign



# Searching for first product
df.iat[1, 1]
# store_navigation()
for row in df['Item'].dropna()[1:]:
    print(row)

    #     first_search(row)
    #     print(scraping_price())
    # else:
    #     subsequent_search(row)
    #     print(scraping_price())



# If in Sprouts column, detect images from Sprouts store only
# Work on adding checkboxes to sheet
# Work on separating these features