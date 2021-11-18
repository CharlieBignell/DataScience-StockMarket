# Data Science - Stock Market Data

This project uses data science to manipulate stock market portfolio data. The project has three Python notebook files, each with a distinct function.

## Cleanup
The broker I use is called Freetrade. They provide transactional data in the form of a single CSV with the following columns:
- **Value Date**: date of transaction
- **Type**: type of transaction e.g. deposit, buy, sell, etc.
- **Details**: text explanation of transaction e.g. '1.5 Tesla Motors Inc (US88160R1014) @ USD 615.10000 (@ 1 USD = 1.38887 GBP) on 04-Mar-2021 20:30:26'
- **Value**: the amount bought/sold/given in GBP. It's signed i.e. outgoings are negative

Although it contains all the data I need, most of the uesful data is packed into the string contained in the 'details' column. Cleanup.ipynb serves to extract all the useful information from this csv file and export it into three files:
- **basic.csv**: all buys/sells with the columns Date, Type, Value, ShareCount, FXRate, Name, and Currency
- **dividend.csv**: all dividend payments with the columns Date, Value, and Name
- **other.csv**: all other transactions e.g. interest, fx fee, deposits etc. with the columns Date, Value, and Type

This file won't be of much use to anyone who isn't trying to clean up transactional data specifically from Freetrade.

## Analyse
This file reads data in the format exported from *cleanup* above. It plots a basic graph of portfolio value over time (along with rolling averages), and outputs basic stats to the console.

# Synthesise
This file creates synthetic trading data in the format exported from *cleanup* above. It takes a number of inputs:
- **Start date and end date**: the date range to synthesise transactions over.
- **Deposit amount**: the total amount of money to trade with.
- **Deposit no.**: the number of individual deposits to spread 'deposit amount' over.
- **FX Rate**: to simplify things, rather than using the correct fx rate at the time of each transaction, a basic fx rate (USD-GBP) is hard-coded and applied to all transactions.
- **Buy no.**: The number of 'buy' transactions to simulate.
- **Min and max spend**: the minimum and maximum percentage (between 0-1) of the current cash balance to spend when generating a buy. Higher max = spend more per buy = more sells (see below). Wider range = more 'noisy' buy values.
- **Max sell**: the maximum percentage (between 0-1) of the current portfolio to sell at any given sell transaction. Sells are currently used to add cash when a 'buy' is not possible due to lack of funds. Therefore the higher this number, the fewer (but larger) sells there will be.
- **Tickers**: the companies to buy/sell.

All of the above have defaults set. For tickers, I chose two different companies each from the sectors technology, food, energy, finance, health, along with two ETFs.