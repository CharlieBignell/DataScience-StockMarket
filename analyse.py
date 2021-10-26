import pandas as pd

df_buys = pd.read_csv('buys.csv')
df_sells = pd.read_csv('sells.csv')
df_deposits = pd.read_csv('deposits.csv')
df_other = pd.read_csv('other.csv')
df_dividend = pd.read_csv('dividend.csv')


# Portfolio summary
totalSpent = df_buys.groupby('Name').agg({'Value': 'sum'})
sharesIn = df_buys.groupby('Name').agg({'ShareCount': 'sum'})['ShareCount']
sharesOut = df_sells.groupby('Name').agg({'ShareCount': 'sum'})['ShareCount']
netShares = (sharesIn - sharesOut).round(2)

print(netShares)

