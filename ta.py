import pymongo
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np
import mplfinance as mpf
import os
from dotenv import load_dotenv

load_dotenv()
client = pymongo.MongoClient(os.environ.get("DB_URL"))
db = client["jse"]
col = db["companies"]


def create_df(ticker):
    items = col.find({"data.ticker": ticker}, {"pv": 1, "_id": 0})
    df = pd.DataFrame(
        data=list(items)[0]["pv"],
        columns=("unix_date", "open", "high", "low", "close", "volume"),
    )
    df["date"] = pd.to_datetime(df["unix_date"], unit="ms")
    df.set_index("unix_date", inplace=True)
    return df


df = create_df("138SL")
# df["rsi"] = df.ta.rsi()
df["rsi_10"] = ta.rsi(close=df.close, length=10)
df["sma_10"] = df.ta.sma(10)
df["sma_50"] = df.ta.sma(50)
df["sma_100"] = df.ta.sma(100)
df["ema_10"] = ta.ema(close=df.close, length=10)
df["ema_10"] = ta.ema(close=df.close, length=10)
df["ema_50"] = ta.ema(close=df.close, length=50)
df["ema_200"] = ta.ema(close=df.close, length=200)

# df["stoch"] = ta.stoch(high=df.high, low=df.low, close=df.close)
# df["bbands"] = df.ta.bbands(close=df.ta.ohlc4(df["close"]))
# apdict = mpf.make_addplot(df["rsi"])
#
# plt.plot(df.date, df.rsi)
# plt.show()
print(df)
# help(ta.stoch)

# fig0 = go.Figure(
#     data=[go.Ohlc(x=df.date, open=df.open, high=df.high, low=df.low, close=df.close)]
# )

# fig0.show()

# fig = go.Figure()

# fig.add_trace(
#     go.Bar(
#         x=df.date,
#         y=df.volume,
#     )
# )

# fig.add_trace(
#     go.Scatter(
#         x=df.date,
#         y=df.close,
#         xperiod="M1",
#         xperiodalignment="middle",
#         hovertemplate="%{y}%{_xother}",
#     )
# )


# fig.show()
