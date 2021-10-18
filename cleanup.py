import pandas as pd

# Read data and rename date column
df_tran = pd.read_csv('transactions_raw.csv')
df_tran.rename(columns={'Value Date': 'Date'}, inplace=True)

############
#   BUYS   #
############

# Get all buys in a single dataframe along with their corresponiding fx fee
df_buys = df_tran.loc[
    (df_tran["Type"] == "BUY") | 
    (df_tran["Type"] == "FX_FEE"), 
    ["Date", "Type", "Details", "Value"]]
df_buys = df_buys.reset_index(drop=True)


#############
#   SELLS   #
#############

# Get all sells in a single dataframe
df_sells = df_tran.loc[df_tran["Type"] == "SELL", ["Date", "Details", "Value"]]
df_sells = df_sells.reset_index(drop=True)


######################
#   OTHER ACTIVITY   #
######################

# Get all deposits in a single dataframe
df_deposit = df_tran.loc[df_tran["Type"] == "DEPOSIT", ["Date", "Value"]]
df_deposit = df_deposit.reset_index(drop=True)

# Put the remaning activity in a separate dataframe. These add up to very little.
df_other = df_tran.loc[
    (df_tran["Type"] == "INTEREST") | 
    (df_tran["Type"] == "INVESTMENT_INCOME") | 
    (df_tran["Type"] == "STAMP_DUTY"), 
    ["Date", "Type", "Details", "Value"]]
df_other = df_other.reset_index(drop=True)


# Make sure all rows have been included in the new dataframes
errorFlag = len(df_tran.index) - len(df_deposit.index) - len(df_buys.index) - len(df_sells.index) - len(df_other.index)
if errorFlag != 0:
    print("ERROR: " + str(errorFlag) + " row(s) missing in new dataframes")

total_deposit = df_deposit['Value'].sum()
total_out = df_buys['Value'].sum()
total_gain = df_sells['Value'].sum()
net_other = df_other['Value'].sum()