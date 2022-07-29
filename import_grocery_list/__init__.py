import pandas as pd

# A simple grocery calculator for the weekly grocery list, base package for Grocery Scraper features
sprouts_grocery_list = pd.read_excel('../Grocery List.xlsx',
                                     sheet_name='Sprouts', index_col=False)
hy_vee_grocery_list = pd.read_excel('../Grocery List.xlsx',
                                    sheet_name='Hy-Vee')

grocery_list = pd.concat([sprouts_grocery_list, hy_vee_grocery_list])
df_both_stores = pd.DataFrame(grocery_list)
df_sprouts = pd.DataFrame(sprouts_grocery_list)
df_hy_vee = pd.DataFrame(hy_vee_grocery_list)


def grocery_calculator(dataframe):
    cost = round(dataframe['Price'] * dataframe['Quantity'], 2)
    grocery_bill = pd.DataFrame.sum(cost)
    bill_after_tax = round(grocery_bill * 0.10 + grocery_bill, 2)
    return bill_after_tax


def grocery_output():
    return '${:,.2f}'.format(grocery_calculator(df_sprouts) + grocery_calculator(df_hy_vee))

