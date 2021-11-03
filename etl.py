from pymongo.message import _first_batch
import requests
from bs4 import BeautifulSoup
import json
from dotenv import load_dotenv
import os
from requests.sessions import Request
import pymongo

load_dotenv()

session = requests.Session()

cookies = {
    "XSRF-TOKEN": "eyJpdiI6InNQakVFbTBSL2NVaGFGNWNJcjJBUFE9PSIsInZhbHVlIjoiNTh5dnYxeTI2SDlBQjRGREw1eEtreVFjM0FOaTJVTnJ3aG85bWl4SG9LdSs2MHROR21OcGo3YkRZTndGVWZyWkV5UU5wY1ZDWFoxVmFxRTJ2akVLenNrYmMzK1doZkpjaDgwR3VwSzlKOW5pSTZINkxCcGp6cUo2RUpOaWlTUG4iLCJtYWMiOiJkNDI0MTVlNzJmMzQzM2ZkM2MyZTA4MjQzZTgwYjg3NTI4Y2ZmNjJmNmExZDhmZDMwOTdiMzZjNmMwN2QzNmU3IiwidGFnIjoiIn0%3D",
    "mymoneyja_session": "eyJpdiI6ImZPYXM4K0UvdmdBTDZHZnBlOWxxU3c9PSIsInZhbHVlIjoiZ0tNbkdNVUNQMGZYdXZKUGpTQ2c5OTRReVd6bnJKcHI2VjRvME1TZlNWeGJCU0QyWU1lMVp2NEx2d1Y3T3FhcU0xR09QOEprc2VhN1BVRURvaWpBQXJpbldzZzRmd0srN2F3RkVsWm1Ed3NDYUhjWHFiakw4R1FzTkVNbWo3eTAiLCJtYWMiOiI3OTE3MTJmZTUxZDMxOTE3N2JiZTIxNjY0N2ZhM2QwODBmOGJjODNhNWNiZDJjMmViY2ZlYTQ3YjA1MGFiYTBkIiwidGFnIjoiIn0%3D",
    "crisp-client%2Fsession%2F595850e5-08f3-4ce7-82e8-129ab88f150c": "session_c4ac7265-44dc-4714-8f37-1f9dae4bfa38",
}

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:93.0) Gecko/20100101 Firefox/93.0",
    "Accept": "text/html, application/xhtml+xml",
    "Accept-Language": "en-US,en;q=0.5",
    "X-Requested-With": "XMLHttpRequest",
    "X-Inertia": "true",
    "X-Inertia-Version": "9e2f6c6666c6f388d3c296e25c362a23",
    "X-XSRF-TOKEN": "eyJpdiI6InQrOUpnZERMR3ZVTHNhWFVZd2hGT1E9PSIsInZhbHVlIjoicDJoa1pIdHRidzJnTlRtcHBaTm83SklpK1ArWGV3ZG1ERU9rdGZXSTBRMWRUQTJHdVBaVE8vL2xWeks3N054MmdhYStaR0VYWWtZODhjLzBQSUhSdnl6OGdkQjhDa2x2ZXFweENFM2MrK0hQdTBkTVBIQ0E5d1Z3WGlkLzFMaWYiLCJtYWMiOiI0ZDAyNGU5OWM2ZTc4NWVmY2E0MjQwOGQ2ZTVkNjc2NWUwMTQwMjNiNzgwMTdhZTBhZGNkZTVkYjI1NmI5ZjQ2IiwidGFnIjoiIn0=",
    "Referer": "https://mymoneyja.com/login",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "TE": "trailers",
}
email = os.environ.get("EMAIL")
password = os.environ.get("PASSWORD")

data = '{"email":{email},"password":{password},"remember":true}'

login_response = session.post(
    "https://mymoneyja.com/login", headers=headers, cookies=cookies, data=data
)

# used to get list of company tickers
response = session.get(
    "https://mymoneyja.com/stock/138SL", headers=headers, data=data, cookies=cookies
)

# get scaped data
stock_data = json.loads(response.content)

companies = {}
companies["138SL"] = True
# saves the companies tickers in a dictionary
for comp in stock_data["props"]["companies"]:
    companies[comp["ticker"]] = True


# splits companies dictionary. This is done because MongoDB as a size limit on each collection
def split_dict_equally(input_dict, chunks=4):
    "Splits dict by keys. Returns a list of dictionaries."
    # prep with empty dicts
    return_list = [dict() for idx in range(chunks)]
    idx = 0
    for k, v in input_dict.items():
        return_list[idx][k] = v
        if idx < chunks - 1:  # indexes start at 0
            idx += 1
        else:
            idx = 0
    return return_list


num_comp = len(companies)
dictionaries = split_dict_equally(companies, num_comp)
test = []
# populates dictionary with trade data
def get_data(dictionary):
    key = list(dictionary.keys())
    key = key[0]
    print(key)
    response2 = session.get(
        "https://mymoneyja.com/stock/{0}".format(key),
        headers=headers,
        data=data,
        cookies=cookies,
    )
    soup = BeautifulSoup(response2.content, "html.parser")
    stock_data = json.loads(soup.text)
    key = {}
    key["data"] = stock_data["props"]["company"]
    # dictionary[key] = stock_data["props"]["company"]
    # creates a price/volume key to store combined  ohlc and volume data
    pv = []
    for i in range(len(stock_data["props"]["company"]["data"]["ohlc"])):
        price = stock_data["props"]["company"]["data"]["ohlc"]
        volume = stock_data["props"]["company"]["data"]["volume"]
        price[i].append(volume[i]["y"])
        pv.append(price[i])
    # dictionary[key]["pv"] = pv
    key["pv"] = pv
    test.append(key)


for dictionary in dictionaries:
    get_data(dictionary)
# k = list(dictionaries[0].keys())
# print(dictionaries[0]["pv"])


# uploads dictionaries as a collection to MongoDb
client = pymongo.MongoClient(os.environ.get("DB_URL"))
db = client["jse"]
col = db["companies"]

# x = col.insert_one(dictionaries[0])
x = col.insert_many(test)
print(x)
