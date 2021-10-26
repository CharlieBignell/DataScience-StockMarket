import pandas as pd
import numpy as np

# Get the data
df_basic = pd.read_csv('./cleaned/basic.csv')
df_other = pd.read_csv('./cleaned/other.csv')
df_dividend = pd.read_csv('./cleaned/dividend.csv')

# Generate a daily summary table from the 'other' dataframe
df_dailySummary = pd.pivot_table(
    df_other, 
    values="Value", 
    index="Date", 
    columns="Type", 
    aggfunc=np.sum).fillna(0)

# Convert buys and sells to same format as daily summary
df_buys = df_basic.loc[df_basic["Type"] == "BUY", ["Date", "Type", "Value"]]
df_sells = df_basic.loc[df_basic["Type"] == "SELL", ["Date", "Type", "Value"]]
df_basicPivot = pd.pivot_table(
    pd.concat([df_buys, df_sells]), 
    values="Value", index="Date", 
    columns="Type", 
    aggfunc=np.sum
).fillna(0)

# pivot dividend table
df_diviPivot = pd.pivot_table(
    df_dividend, 
    values="Value", index="Date",  
    aggfunc=np.sum
).fillna(0)

# Concatenate daily summary with buys and sells
df_dailySummary = pd.concat([df_dailySummary, df_basicPivot, df_diviPivot], axis=1).fillna(0)

# Format daily summary
df_dailySummary = df_dailySummary.rename(columns={"BUY": "Total Bought", "SELL": "Total Sold"})
df_dailySummary = df_dailySummary
df_dailySummary['Net Income']= df_dailySummary.sum(axis=1)
print(df_dailySummary)

# Calculate net shares
myDate = "14/08/2020"
df_buys = df_basic.loc[df_basic["Type"] == "BUY", ["Name", "ShareCount"]]
df_sells = df_basic.loc[df_basic["Type"] == "SELL", ["Name", "ShareCount"]]
sharesIn = df_buys.groupby('Name').agg({'ShareCount': 'sum'})['ShareCount']
sharesOut = df_sells.groupby('Name').agg({'ShareCount': 'sum'})['ShareCount']
netShares = (sharesIn - sharesOut).round(5)
# print(netShares)

df_dailySummary.to_csv('./outputs/daily.csv', index=True)