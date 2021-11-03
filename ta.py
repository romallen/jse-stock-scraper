import pymongo
import pandas as pd
import pandas_ta as ta
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

load_dotenv()
client = pymongo.MongoClient(os.environ.get("DB_URL"))
db = client["jse"]
col = db["companies"]

items = col.find({"data.ticker": "FESCO"}, {"pv": 1, "_id": 0})
stock = []
# for x in items:
# stock = x["pv"]
# print(x)

df = pd.DataFrame(
    data=list(items)[0]["pv"],
    columns=("unix_date", "open", "high", "low", "close", "volume"),
)
df["date"] = pd.to_datetime(df["unix_date"], unit="ms")

# df["rsi"] = ta.rsi(close=df.close, length=10)
df["rsi"] = df.ta.rsi()

plt.plot(df.date, df.rsi)
print(df)
plt.show()
# ta.mom
# df["rsi"] = ta.momentum.RSIIndicator(df[4], window=14).rsi()
# plt.plot(df[0], df["rsi"])
# plt.show()
