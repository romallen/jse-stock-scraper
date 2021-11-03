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

items = col.find({"data.ticker": "FESCO"})
stock = []
for x in items:
    stock = x["pv"]

# data=stock, columns=("Date", "Open", "High", "Low", "Close", "Volume")
df = pd.DataFrame()

print(df)

# ta.mom
# df["rsi"] = ta.momentum.RSIIndicator(df[4], window=14).rsi()
# plt.plot(df[0], df["rsi"])
# plt.show()
