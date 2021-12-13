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
    "XSRF-TOKEN": "eyJpdiI6IjE0Ui90dUY4djlqVHBnVWpERldOMWc9PSIsInZhbHVlIjoiOFAvT1IzQzJGbnJSdFNJdW1MalZScnUvUXJuNXdYTEdzbXM3d2VFdzlKa2VCY0loRGRoTDRNYm9oUWN4RUNYV1BYczR0bHdaQmhvbEhMNjFQZ25ncEcrVitkSnpzZUl3YXFYSHRIYkdBS2VqZEhRMm5Hc096Z052T1hIYlRqQ2kiLCJtYWMiOiI2ZmQ3NTg2MDM5NjhjNmJiZWQyMjgwZDVjNzYwOWQxNDUyYTA0NGY4ZWQ2YTI1Mzc4NWUyYzJjZGMxNjUwNTI1IiwidGFnIjoiIn0%3D",
    "mymoneyja_session": "eyJpdiI6IktVOGNmbWZYV3pzRlZIalZrNWNEalE9PSIsInZhbHVlIjoiNklWb29hZDFEcVlQYTZ1eTFpUkpTL0crQnhCWjRCU3A5cVdOTWNBV3ZDc0VkZ0k3M0ZTUkxUTURUTEpkTjJWRERTTlVUOCtqZzBRYWlEeWRVN0ROVzF6cVRnQnVOeWV2Q0NjdVV5SlhIc0M4Z09FbXR0aUtES09UTEgwNmxZME4iLCJtYWMiOiI4ZDE4M2FkMDYyMjA4ZmNmOTRiNjQxMDFkNzJhOTVlNzZkYzUxY2E3NjY3NDJmNzEwODNjMTA5NDRlY2QyMmRlIiwidGFnIjoiIn0%3D",
    "remember_web_3dc7a913ef5fd4b890ecabe3487085573e16cf82": "eyJpdiI6InJlenR4bVpiSE15RXJWUURrdW1oYkE9PSIsInZhbHVlIjoiTktCQ3EzWUFVYnd1bnc4YjdybzIzYlIxUWFiNFNMRENUSy9ZQUhQeUhobXZvcHBJT1pZSDVNSUQxSTVGcklhdytrbTd3anRDeDJhR0dTSjliL1BidzdPeXpKU1JlNFI2TEdELzlpUmZyWUZyQjVFVkxRbktWUG5vNTFxQUdIalpadHpvKy9ubHR2d1o2RUJ3UnlrSTNjamZxalNRbXJvSjNiZkswaG50dk1GZkFpRFlrTTNibit6ejB6L2o0ZldDSWZFYXpPNjBFQVMvNCtVZWpabkpxWUpFVGswN2U3NHFEekZRT1BjaFVuWT0iLCJtYWMiOiIwOTliNGZjNDZmMWE2MWFmYTA0MjJjMjczNGEyZDliZjFhN2FmOTVhMjU1NTE3MmY1NGM5YzMyZjE3MzM4ODgwIiwidGFnIjoiIn0%3D",
}


session.headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:95.0) Gecko/20100101 Firefox/95.0",
    "Accept": "text/html, application/xhtml+xml",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "X-Requested-With": "XMLHttpRequest",
    "X-Inertia": "true",
    "X-Inertia-Version": "eaab6f8db0b109568ae5e7468dbd534a",
    "X-XSRF-TOKEN": "eyJpdiI6IjlqSkhZUXVscnJKdnpZMllFRUNwNHc9PSIsInZhbHVlIjoiN2EwTjZ3WjZ0VS9UWEk0RXlyTWcreENGaHFrY3FKQ250T3k5NGVibW1mRitOMkI1elVXZVNQSlRxcVAwc0xielhzOUZrcUtzcHlqcU1vSDdXSnJXdGpZMmUzN0xsN09XMExBcFl5RC9uTGNqT04xVzExQzB3ZEJLR1ZmaFNyNUUiLCJtYWMiOiI1YmMwMzNiNzZjYTI4OWIwZmU3Yjg5M2I1MWQyZDgwZDFlMTg5ZTQwZDg0ODVjNWQ2NzgyZjFkNDM5YzBmODgzIiwidGFnIjoiIn0=",
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


def login():

    login_response = session.post(
        "https://mymoneyja.com/login",
        data=data,
        cookies=cookies,
        headers=session.headers,
    )
    # print(login_response.headers)
    # ession.cookies = session.cookies.get_dict()
    print(login_response.headers)

    # used to get list of company tickers
    # response = session.get("https://mymoneyja.com/stock/138SL", data=data)
    # soup = BeautifulSoup(response, "html.parser")
    # print(response.text)

    # print(response.content)
    # get scaped data
    # return json.loads(response.content)


# login()
response = session.get(
    "https://mymoneyja.com/stock/138SL", cookies=cookies, headers=session.headers
)

# get scaped data for tickers
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
documents = []
# populates dictionary with trade data
def get_data(dictionary):
    key = list(dictionary.keys())
    key = key[0]
    print(key)
    response2 = session.get(
        "https://mymoneyja.com/stock/{0}".format(key),
        cookies=cookies,
        headers=session.headers,
    )
    soup = BeautifulSoup(response2.content, "html.parser")
    stock_data = json.loads(soup.text)
    key = {}
    #key["data"] = stock_data["props"]["company"]
    # dictionary[key] = stock_data["props"]["company"]
    # creates a price/volume key to store combined  ohlc and volume data
    # pv = []
    # for i in range(len(stock_data["props"]["company"]["data"]["ohlc"])):
       
        # price[i].append(volume[i]["y"])
        # pv.append(price[i])
    # dictionary[key]["pv"] = pv
    # key["pv"] = pv
    key["name"] = stock_data["props"]["company"]["name"]
    key["ticker"] = stock_data["props"]["company"]["ticker"]
    key["close_prices"] = stock_data["props"]["company"]["data"]["close_prices"]
    key["ohlc"] = stock_data["props"]["company"]["data"]["ohlc"]
    key["volume"] = stock_data["props"]["company"]["data"]["volume"]
    documents.append(key)


for dictionary in dictionaries:
    get_data(dictionary)


# uploads dictionaries as a collection to MongoDb
client = pymongo.MongoClient(os.environ.get("DB_URL"))
db = client["jse"]
coll = db["companies"]

x = coll.delete_many({})
print(x.deleted_count, " documents deleted.")
y = coll.insert_many(documents)
print(y)


# x = coll.insert_one(documents[0])
# x = col.insert_many(documents)
# print(x)
