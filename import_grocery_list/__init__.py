import pandas as pd

# A simple grocery calculator for the weekly grocery list, base package for Grocery Scraper features
sprouts_grocery_list = pd.read_excel('../Grocery List.xlsx',
                                     sheet_name='Sprouts')

df_sprouts = pd.DataFrame(sprouts_grocery_list)


def grocery_calculator(dataframe):
    cost = round(dataframe['Price'] * dataframe['Quantity'], 2)
    grocery_bill = pd.DataFrame.sum(cost)
    bill_after_tax = round(grocery_bill * 0.10 + grocery_bill, 2)
    return bill_after_tax


def grocery_output():
    return '${:,.2f}'.format(grocery_calculator(df_sprouts))

