import pandas as pd

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


# If in Sprouts column, detect images from Sprouts store only
# Work on adding checkboxes to sheet
# Work on separating these features