import pandas as pd
import numpy as np
import yfinance as yf

# Get the data
df_basic = pd.read_csv('./cleaned/basic.csv')
df_other = pd.read_csv('./cleaned/other.csv')
df_dividend = pd.read_csv('./cleaned/dividend.csv')
df_basic['Date'] = pd.to_datetime(df_basic['Date'])
df_other['Date'] = pd.to_datetime(df_other['Date'])
df_dividend['Date'] = pd.to_datetime(df_dividend['Date'])

# Get a list of all tickers traded
tickers_all = df_basic['Name'].unique()


# Account for any stock splits
allSplits = []
for ticker in tickers_all:

    # Get the split and convert to a df
    splits = yf.Ticker(ticker).splits
    df_split = pd.DataFrame({'Date':splits.index, 'Split':splits.values})
    df_split["Name"] = ticker

    # If there was a split, append the df to allSplits. The ignoring of PFE is a quirk with a spin off they did with Viatris in 2020. This is a bad fix but it'll do for now
    if len(df_split.index) != 0 and ticker != "PFE":
        allSplits.append(df_split)

allSplits = pd.concat(allSplits)

for index, row in allSplits.iterrows():
    df_basic.loc[(df_basic["Name"] == row["Name"]) & (df_basic["Date"] < row["Date"]), ["ShareCount"]] = (df_basic['ShareCount'] * row["Split"]).round(6)


#Split buys and sells into separate dataframes
df_buys = df_basic.loc[df_basic["Type"] == "BUY"]
df_sells = df_basic.loc[df_basic["Type"] == "SELL"]

###########################
# Net Shares on Given Day #
###########################
def getShareCount(day = pd.to_datetime("today")):

    # Get the buys and sells for each day before the given date
    df_buysInRange = df_buys.loc[df_basic["Date"] < day, ["Date", "Name", "ShareCount"]]
    df_sellsInRange = df_sells.loc[df_basic["Date"] < day, ["Date", "Name", "ShareCount"]]

    # Any missing sells, i.e. any stock we've bought but not sold any of, need to still be in the resulting 'sell' df
    df_emptySells = df_buysInRange.copy()
    df_emptySells["ShareCount"] = 0
    df_sellsInRange = pd.concat([df_sellsInRange, df_emptySells])

    # Aggregate to get total shares in and out
    sharesIn = df_buysInRange.groupby('Name').agg({'ShareCount': 'sum'})['ShareCount']
    sharesOut = df_sellsInRange.groupby('Name').agg({'ShareCount': 'sum'})['ShareCount']

    # Calculate net shares
    netShares_all = (sharesIn - sharesOut).round(5).to_frame(name="ShareCount")
    netShares = netShares_all.loc[netShares_all["ShareCount"] != 0]

    return netShares

# A list of current tickers
tickers_current = getShareCount().index.values.tolist()

# A series of current tickers with the number of shares
tickerShares_current = getShareCount()

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
df_basicPivot = pd.pivot_table(
    pd.concat([df_buys[["Date", "Type", "Value"]], df_sells[["Date", "Type", "Value"]]]), 
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

df_dailySummary.to_csv('./outputs/daily.csv', index=True)