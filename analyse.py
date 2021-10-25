import pandas as pd

df_buys = pd.read_csv('buys.csv')
df_sells = pd.read_csv('sells.csv')
df_deposits = pd.read_csv('deposits.csv')
df_other = pd.read_csv('other.csv')
df_dividend = pd.read_csv('dividend.csv')

# Ticker summary
# date of first buy, total bought, total sold, current amount holding, 

# Portfolio summary
# One row per ticker
# Name, shares, money in, money out, net spend

# day/week/month summary
# ticker, net shares, net £