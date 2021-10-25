import pandas as pd

# transactions_raw columns:
# Value Date: date of transaction
# Type: type of transaction e.g. deposit, buy, sell, etc.
# Details: text explanation of transaction e.g. '1.5 Tesla Motors Inc (US88160R1014) @ USD 615.10000 (@ 1 USD = 1.38887 GBP) on 04-Mar-2021 20:30:26'
# Value: the amount bought/sold/given in GBP. It's signed i.e. outgoings are negative

# Read data and rename date column
df_tran = pd.read_csv('transactions_raw.csv')
df_tran.rename(columns={'Value Date': 'Date'}, inplace=True)


def removeShareCount(string):
    return " ".join(string.split()[1:])


def format(df):
    # Use regular expressions to extract the different components of from the 'details' column
    df["ShareCount"] = df["Details"].str.extract(r'(^\d+[.]\d+|^\d+[^\\])')
    df["FXRate"] = df["Details"].str.extract(r'(\(@.+?\))')
    df["ISIN"] = df["Details"].str.extract(r'([A-Z]{2}[A-Z0-9]{9}[0-9]{1})')
    df["Name"] = df["Details"].str.extract(r'(.+(?= \([A-Z]{2}[A-Z0-9]{9}[0-9]{1}))')

    # 'name' still contains the share count which we need to remove
    df["Name"] = df["Name"].apply(removeShareCount)

    df["Currency"] = df["FXRate"].str.extract(r'([A-Z]+(?=\)))')
    df["FXRate"] = df["FXRate"].str.extract(r'(= \d+.\d+)')
    df["FXRate"] = df["FXRate"].str[2:]
    df.loc[df["FXRate"].isnull(), 'FXRate'] = "1"
    df.loc[df["Currency"].isnull(), 'Currency'] = "GBP"

    # Now that we've extracted all we need, drop the 'Details'  and 'Type' columns
    df.drop(columns=["Details", "Type"], inplace=True)

    # Convert numeric columns
    df[["ShareCount", "Value", "FXRate"]] = df[[
        "ShareCount", "Value", "FXRate"]].apply(pd.to_numeric)


# Get all buys in a single dataframe, and format
df_buys = df_tran.loc[df_tran["Type"] == "BUY", ["Date", "Type", "Details", "Value"]]
format(df_buys)

# Convert the value to positive i.e. amount spent, rather than net balance, as this is more intuitive now that we've separated buying and selling
df_buys["Value"] = df_buys["Value"]*-1

# Get all sells in a single dataframe
df_sells = df_tran.loc[df_tran["Type"] == "SELL", ["Date", "Type", "Details", "Value"]]
format(df_sells)

# Get all deposits in a single dataframe
df_deposit = df_tran.loc[df_tran["Type"] == "DEPOSIT", ["Date", "Value"]]

# Get all dividends in a single dataframe
df_dividend = df_tran.loc[df_tran["Type"] == "INVESTMENT_INCOME", ["Date", "Details", "Value"]]
df_dividend["ISIN"] = df_dividend["Details"].str.extract(r'([A-Z]{2}[A-Z0-9]{9}[0-9]{1})')
df_dividend["Name"] = df_dividend["Details"].str.extract(r'(m .+(?= \([A-Z]{2}[A-Z0-9]{9}[0-9]{1}))')
df_dividend["Name"] = df_dividend["Name"].apply(removeShareCount)
df_dividend.drop(columns=["Details"], inplace=True)

# Put the remaning activity in a separate dataframe. The value of each transaction here tends to be very small
df_interest = df_tran.loc[df_tran["Type"] == "INTEREST", ["Date", "Value"]]
df_fx = df_tran.loc[df_tran["Type"] == "FX_FEE", ["Date", "Type", "Value"]]
df_stamp = df_tran.loc[df_tran["Type"] == "STAMP_DUTY", ["Date", "Type", "Value"]]

df_stamp["Type"] = "Stamp Duty"
df_interest["Type"] = "Interest"
df_fx["Type"] = "FX Fee"

df_other = pd.concat([df_stamp, df_interest, df_fx])
df_other = df_other.reset_index(drop=True)

df_buys.to_csv('buys.csv', index=False)
df_sells.to_csv('sells.csv', index=False)
df_deposit.to_csv('deposits.csv', index=False)
df_dividend.to_csv('dividend.csv', index=False)
df_other.to_csv('other.csv', index=False)

# Make sure all rows have been included in the new dataframes
errorFlag = len(df_tran.index) - len(df_deposit.index) - len(df_buys.index) - len(df_sells.index) - len(df_dividend.index) - len(df_other.index)
if errorFlag != 0:
    print("ERROR: " + str(errorFlag) + " row(s) missing in new dataframes")
