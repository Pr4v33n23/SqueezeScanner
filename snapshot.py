import yfinance as yf
from yahooquery import Screener
import pandas as pd


def get_data():
    crypto_ticker_list = Screener().get_screeners('all_cryptocurrencies_us', count=100)
    for key, value in pd.json_normalize(crypto_ticker_list, sep='_')['all_cryptocurrencies_us_quotes'].items():
        df_flatten = pd.json_normalize(value, sep="_")
        df_flatten['symbol'].to_csv("symbols.csv", header=False, index=False)
        for ticker in df_flatten['symbol']:
            data = yf.download(ticker, period="60d", interval="15m")
            data.to_csv(f"datasets/{ticker}.csv")
