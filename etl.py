from pymongo.message import _first_batch
import requests
from bs4 import BeautifulSoup
import json
from dotenv import load_dotenv
import os
from requests.sessions import Request
import pymongo
import boto3


load_dotenv()
s3 = boto3.resource('s3')

session = requests.Session()
cookies = {
     'remember_web_3dc7a913ef5fd4b890ecabe3487085573e16cf82': 'eyJpdiI6IjJoZmpYWjFYOENjQjQ1Lyt2TVpNSEE9PSIsInZhbHVlIjoiRkRCSkJwcXpvZG12MTNiWmhZOTU0cmdqQU9rUGgrQUw5V3dkU01HTENlK3lYdmJHYkVibldxWDJENmNlK2w1QzJHSStTdzdHVzhYYXE2UFUwdnEwRTZGVzQwUUxrKzErMHoyRTdreC9ra3NDL29lNkVSaWRVanZIVFNBTmZwamJOU2RmRGJtbG1FYWdoVnJ6M0RKV3pnR2s1SkhJUW9mQUtJQmdFRSsxZWdISWNHNnRnNFlLcVkwbnJwTXNYY2xCZ1h3ak9MeDV4MGZPUHVJUmJwNGlDYng5YmNOekxlUFcwTElLdEFKWjJkdz0iLCJtYWMiOiJiYjRjYjdkNWI2MzQ0NTY0Y2Q1Y2FkZDAyYTc3NGVjNDMxZWZjNzZjZjVkZGQwMzllODBkYjUzODE1MmRhOTZjIiwidGFnIjoiIn0%3D',
    'XSRF-TOKEN': 'eyJpdiI6InQrV1N3bDBzS2ZxWUJHNEJXRFhSc2c9PSIsInZhbHVlIjoiYkxHN3VKcWovS2M3RmdSQmZIMS95N0E5TTRoMDRHU2M1dTArYTdPSTdkRWxJVGNwRjZ5R3BrSmtGRnhwSThlSHZXQkhyTDBRL28rYVJ3ZFVWMFhNdWdlalMxbjNqT2pEQnc1KzRNM0x1NHdxOWRRZEp6bVNxSUVpZ1hNNDBhalIiLCJtYWMiOiI1NDEwOTc2MTEwMGE0MjkxZDg5N2UyZDQzYWIxNTgwMWYzOWQwNWFjZjMxMWFiMDg3NWIyMjBiMzMwMjkyM2VlIiwidGFnIjoiIn0%3D',
    'mymoneyja_session': 'eyJpdiI6ImgyTXUyUlRwUXpBL2xCbmJjTGRPTlE9PSIsInZhbHVlIjoia2FId09SemV4RGt2SmpKZ2lPVURCR0ZDRnRVclAvSW5YemprMk1FNVdheUdJRjI0RDlNTkVhTXBwOHhmZ0VGcndLMDN3MUhmZnh2Wkp0ZHhVL3Vta296cUIvR0QxR3hyR2ZyYkMwZXQxOVBueEM3UE9jdFdjYkN2dHlQSDNUYy8iLCJtYWMiOiJlODQ0MTE5NGY0MWMyYzU4ZjU0ZmIyM2NlZWRlMWUxZTQ4ODU5NmExYzUyODNkY2VjOTIwOTc5ZWMwZDIwMjc3IiwidGFnIjoiIn0%3D',
    'crisp-client%2Fsession%2F595850e5-08f3-4ce7-82e8-129ab88f150c': 'session_e4c573dc-144c-440f-bb5e-2672ee260f07',

    }


session.headers = {
     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:95.0) Gecko/20100101 Firefox/95.0',
    'Accept': 'text/html, application/xhtml+xml',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'X-Requested-With': 'XMLHttpRequest',
    'X-Inertia': 'true',
    'X-Inertia-Version': '0ef7f1ebf4673ce29938a6c1c794971d',
    'Content-Type': 'application/json',
    'X-XSRF-TOKEN': 'eyJpdiI6InQrV1N3bDBzS2ZxWUJHNEJXRFhSc2c9PSIsInZhbHVlIjoiYkxHN3VKcWovS2M3RmdSQmZIMS95N0E5TTRoMDRHU2M1dTArYTdPSTdkRWxJVGNwRjZ5R3BrSmtGRnhwSThlSHZXQkhyTDBRL28rYVJ3ZFVWMFhNdWdlalMxbjNqT2pEQnc1KzRNM0x1NHdxOWRRZEp6bVNxSUVpZ1hNNDBhalIiLCJtYWMiOiI1NDEwOTc2MTEwMGE0MjkxZDg5N2UyZDQzYWIxNTgwMWYzOWQwNWFjZjMxMWFiMDg3NWIyMjBiMzMwMjkyM2VlIiwidGFnIjoiIn0=',
    'Connection': 'keep-alive',
    'Referer': 'https://mymoneyja.com/market',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'TE': 'trailers',
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

    print(login_response.headers)



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
    keystr = list(dictionary.keys())
    keystr = keystr[0]
    print(keystr)
    response2 = session.get(
        "https://mymoneyja.com/stock/{0}".format(keystr),
        cookies=cookies,
        headers=session.headers,
    )
    soup = BeautifulSoup(response2.content, "html.parser")
    stock_data = json.loads(soup.text)
    key = {}
   
    key["name"] = stock_data["props"]["company"]["name"]
    key["ticker"] = stock_data["props"]["company"]["ticker"]
    key["blurb"] = stock_data["props"]["company"]["blurb"]
    #key["close_prices"] = stock_data["props"]["company"]["data"]["close_prices"]
    key["ohlc"] = stock_data["props"]["company"]["data"]["ohlc"]
    key["volume"] = stock_data["props"]["company"]["data"]["volume"]
    documents.append(key)
    
    stockChartData = []
    stockChartData.append([key["name"], key["ticker"], key["blurb"]])
    for i in range(len(stock_data["props"]["company"]["data"]["ohlc"])):
        price = key["ohlc"][i]
        vol = key["volume"][i]["volume"]
        price.append(vol)
        stockChartData.append(price)
    
    s3object = s3.Object('romallen.com', f'json/{keystr}-data.json')
    s3object.put( Body=(bytes(json.dumps(stockChartData).encode('UTF-8'))), ContentType='application/json' )



for dictionary in dictionaries:
    get_data(dictionary)


# uploads dictionaries as a collection to MongoDb
client = pymongo.MongoClient(os.environ.get("DB_URL"))
db = client["jse"]
coll = db["companies"]

# x = coll.delete_many({})
# print(x.deleted_count, " documents deleted.")
y = coll.insert_many(documents)
print(y)

