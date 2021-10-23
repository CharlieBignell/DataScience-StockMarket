import pandas as pd

# transactions_raw columns:
# Value Date: date of transaction
# Type: type of transaction e.g. deposit, buy, sell, etc.
# Details: text explanation of transaction e.g. '1.5 Tesla Motors Inc (US88160R1014) @ USD 615.10000 (@ 1 USD = 1.38887 GBP) on 04-Mar-2021 20:30:26'
# Value: the amount bought/sold/given. It's signed i.e. outgoings are negative

# Read data and rename date column
df_tran = pd.read_csv('transactions_raw.csv')
df_tran.rename(columns={'Value Date': 'Date'}, inplace=True)


############
#   BUYS   #
############

# Get all buys in a single dataframe
df_buys = df_tran.loc[df_tran["Type"] == "BUY", ["Date", "Type", "Details", "Value"]]
df_buys = df_buys.reset_index(drop=True)


#############
#   SELLS   #
#############

# Get all sells in a single dataframe
df_sells = df_tran.loc[df_tran["Type"] == "SELL", ["Date", "Type", "Details", "Value"]]
df_sells = df_sells.reset_index(drop=True)


################
#   DEPOSITS   #
################

# Get all deposits in a single dataframe
df_deposit = df_tran.loc[df_tran["Type"] == "DEPOSIT", ["Date", "Value"]]
df_deposit = df_deposit.reset_index(drop=True)


######################
#   OTHER ACTIVITY   #
######################

# Put the remaning activity in a separate dataframe. The value of each transaction here tends to be very small
df_other = df_tran.loc[
    (df_tran["Type"] == "INTEREST") | 
    (df_tran["Type"] == "INVESTMENT_INCOME") | 
    (df_tran["Type"] == "FX_FEE") |
    (df_tran["Type"] == "STAMP_DUTY"), 
    ["Date", "Type", "Details", "Value"]]
df_other = df_other.reset_index(drop=True)

print(df_buys)
print(df_sells)

# Make sure all rows have been included in the new dataframes
errorFlag = len(df_tran.index) - len(df_deposit.index) - len(df_buys.index) - len(df_sells.index) - len(df_other.index)
if errorFlag != 0:
    print("ERROR: " + str(errorFlag) + " row(s) missing in new dataframes")