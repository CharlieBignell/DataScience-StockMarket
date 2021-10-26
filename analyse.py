import pandas as pd
import numpy as np

# Get the data
df_basic = pd.read_csv('basic.csv')
df_other = pd.read_csv('other.csv')
df_dividend = pd.read_csv('dividend.csv')

# Generate a daily summary table from the 'other' dataframe
df_dailySummary = pd.pivot_table(df_other, values="Value", index="Date", columns="Type", aggfunc=np.sum).fillna(0)
df_dailySummary[["FX Fee", "Deposit", "Interest", "Stamp Duty"]] = df_dailySummary[["FX Fee", "Deposit", "Interest", "Stamp Duty"]].round(2)

# # Add bought to daily
# df_buys = df_basic.loc[df_basic["Type"] == "BUY", ["Date", "Value"]]
# df_sells = df_basic.loc[df_basic["Type"] == "SELL", ["Date", "Value"]]

# print(df_sells)