import pandas as pd
import numpy as np

# transactions_raw columns:
# Value Date: date of transaction
# Type: type of transaction e.g. deposit, buy, sell, etc.
# Details: text explanation of transaction e.g. '1.5 Tesla Motors Inc (US88160R1014) @ USD 615.10000 (@ 1 USD = 1.38887 GBP) on 04-Mar-2021 20:30:26'
# Value: the amount bought/sold/given in GBP. It's signed i.e. outgoings are negative

# Read data and format the date column
df_tran = pd.read_csv('./inputs/transactions_raw.csv')
df_tran.rename(columns={'Value Date': 'Date'}, inplace=True)
df_tran['Date'] = pd.to_datetime(df_tran['Date'], format="%d/%m/%Y")

#########
# BASIC #
#########

# Get all buys and sells in a single dataframe
df_basic = df_tran.loc[(df_tran["Type"] == "BUY") | (df_tran["Type"] == "SELL"), ["Date", "Type", "Details", "Value"]]

# Use regular expressions to extract the different components of from the 'details' column
df_basic["ShareCount"] = df_basic["Details"].str.extract(r'(^\d+[.]\d+|^\d+[^\\])')
df_basic["FXRate"] = df_basic["Details"].str.extract(r'(\(@.+?\))')
df_basic["ISIN"] = df_basic["Details"].str.extract(r'([A-Z]{2}[A-Z0-9]{9}[0-9]{1})')
df_basic["Name"] = df_basic["Details"].str.extract(r'(.+(?= \([A-Z]{2}[A-Z0-9]{9}[0-9]{1}))')

# 'name' still contains the share count which we need to remove
def removeShareCount(string):
    return " ".join(string.split()[1:])
df_basic["Name"] = df_basic["Name"].apply(removeShareCount)

df_basic["Currency"] = df_basic["FXRate"].str.extract(r'([A-Z]+(?=\)))')
df_basic["FXRate"] = df_basic["FXRate"].str.extract(r'(= \d+.\d+)')
df_basic["FXRate"] = df_basic["FXRate"].str[2:]
df_basic.loc[df_basic["FXRate"].isnull(), 'FXRate'] = "1"
df_basic.loc[df_basic["Currency"].isnull(), 'Currency'] = "GBP"

# Now that we've extracted all we need, drop the 'Details' column
df_basic.drop(columns=["Details"], inplace=True)

# Convert numeric columns
df_basic[["ShareCount", "Value", "FXRate"]] = df_basic[["ShareCount", "Value", "FXRate"]].apply(pd.to_numeric)

#############
# Dividends #
#############

# Get all dividends in a single dataframe
df_dividend = df_tran.loc[df_tran["Type"] == "INVESTMENT_INCOME", ["Date", "Details", "Value"]]
df_dividend["ISIN"] = df_dividend["Details"].str.extract(r'([A-Z]{2}[A-Z0-9]{9}[0-9]{1})')
df_dividend["Name"] = df_dividend["Details"].str.extract(r'(m .+(?= \([A-Z]{2}[A-Z0-9]{9}[0-9]{1}))')
df_dividend["Name"] = df_dividend["Name"].apply(removeShareCount)
df_dividend.drop(columns=["Details"], inplace=True)

#########
# Other #
#########

# Put the remaning activity in a separate dataframe. The value of each transaction here tends to be very small
df_interest = df_tran.loc[df_tran["Type"] == "INTEREST", ["Date", "Value"]]
df_fx = df_tran.loc[df_tran["Type"] == "FX_FEE", ["Date", "Value"]]
df_stamp = df_tran.loc[df_tran["Type"] == "STAMP_DUTY", ["Date", "Value"]]
df_deposit = df_tran.loc[df_tran["Type"] == "DEPOSIT", ["Date", "Value"]]

df_stamp["Type"] = "Stamp Duty"
df_interest["Type"] = "Interest"
df_fx["Type"] = "FX Fee"
df_deposit["Type"] = "Deposit"

df_other = pd.concat([df_stamp, df_interest, df_fx, df_deposit])
df_other = df_other.reset_index(drop=True)

# Output dataframes to CSV
df_basic.to_csv('./cleaned/basic.csv', index=False)
df_dividend.to_csv('./cleaned/dividend.csv', index=False)
df_other.to_csv('./cleaned/other.csv', index=True)
