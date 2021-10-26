import pandas as pd
import numpy as np

# Get the data
df_basic = pd.read_csv('./cleaned/basic.csv')
df_other = pd.read_csv('./cleaned/other.csv')
df_dividend = pd.read_csv('./cleaned/dividend.csv')
df_basic['Date'] = pd.to_datetime(df_basic['Date'])
df_other['Date'] = pd.to_datetime(df_other['Date'])
df_dividend['Date'] = pd.to_datetime(df_dividend['Date'])

#################
# Daily Summary #
#################

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

###########################
# Net Shares on Given Day #
###########################

date = pd.to_datetime("2021-10-26")

# Get the buys and sells for each day before the given date
df_buysInRange = df_basic.loc[(df_basic["Type"] == "BUY") & (df_basic["Date"] < date), ["Date", "Name", "ShareCount"]]
df_sellsInRange = df_basic.loc[(df_basic["Type"] == "SELL") & (df_basic["Date"] < date), ["Date", "Name", "ShareCount"]]

# Any missing sells, i.e. any stock we've bought but not sold any of, need to still be in the resulting 'sell' df
df_emptySells = df_buysInRange.copy()
df_emptySells["ShareCount"] = 0
df_sellsInRange = pd.concat([df_sellsInRange, df_emptySells])

# Aggregate to get total shares in and out
sharesIn = df_buysInRange.groupby('Name').agg({'ShareCount': 'sum'})['ShareCount']
sharesOut = df_sellsInRange.groupby('Name').agg({'ShareCount': 'sum'})['ShareCount']

# Calculate net shares
netShares = (sharesIn - sharesOut).round(5).to_frame(name="ShareCount")
netShares = netShares.loc[netShares["ShareCount"] != 0]

df_dailySummary.to_csv('./outputs/daily.csv', index=True)