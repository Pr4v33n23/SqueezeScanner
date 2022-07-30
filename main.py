import pandas
import snapshot
import plotly.graph_objects as go

snapshot.get_data()
with open("symbols.csv") as f:
    for symbol in f.read().splitlines():
        df = pandas.read_csv(f"datasets/{symbol}.csv")
        if df.empty:
            print("dataset is empty.")

        df['20sma'] = df['Close'].rolling(window=20).mean()
        df['stddev'] = df['Close'].rolling(window=20).std()
        df['lower_band'] = df['20sma'] - 2 * df['stddev']
        df['upper_band'] = df['20sma'] + 2 * df['stddev']
        df['TR'] = abs(df['High'] - df['Low'])
        df['ATR'] = df['TR'].rolling(window=20).mean()
        df['lower_keltner'] = df['20sma'] - (df['ATR'] * 1.5)
        df['upper_keltner'] = df['20sma'] + (df['ATR'] * 1.5)

        def in_squeeze(df):
            return df['lower_band'] > df['lower_keltner'] and df['upper_band'] < df['upper_keltner']

        df['squeeze_on'] = df.apply(in_squeeze, axis=1)

        if df.iloc[-3]['squeeze_on'] and not df.iloc[-1]['squeeze_on']:
            print(f"{symbol} is coming out of the squeeze")

