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
   'XSRF-TOKEN': 'eyJpdiI6Ik1NWFhIS1dHcGtHdzFreDRXVmxhVXc9PSIsInZhbHVlIjoicmxoTGFEMnZvTjA2STQrRy9sYm1sS1ErU0ptMkxMQThKM2E0YXV4Y0VITkRYczlycHM3NHFSOHl4czFmYjNRVzFCTjNxSjRqYzlGVXUraW1QSjdNdWxubU96UzFvKzVHeFdtRmJyZmpyUG40MjUzRWlIQmZxNG0vZ0I0bUI4K1UiLCJtYWMiOiIyMzNmZWZiZTE4MGM4NjM1NGU1ZWU1MTZlYmU0ZmIzMzhhZmYyMDliMTU2NDJlNzA0NjA1MmMyY2U0ZTQyNzYzIiwidGFnIjoiIn0%3D',
    'mymoneyja_session': 'eyJpdiI6Ijg3UWdTWDAyMmRPVlBUL0g0K24zcHc9PSIsInZhbHVlIjoiVDl5bEVqcVN5TW1qdFEyY3p5SFVLaEIzR09KRGcydkR0R0FTTSswcmpsak94SnFnbEJaM0I0d3NsMXVIWDJ1NXFIa3gxSm4rbWNmd1h2b1R5UmdXdDJmVTZXTEdzNEhQZmp0UnQ5UjllODJkcW9hdy9iQWdyM1NlVFo3U0Z1djMiLCJtYWMiOiJiNTYxMDZkYmNlZTNjZWM4MjdmOTY2NThlMGE5YzdkNjM5MDEzYjBlNjhmOTIwMTAzZDMyMjU4NGI1NjhjMGQyIiwidGFnIjoiIn0%3D',
    'crisp-client%2Fsession%2F595850e5-08f3-4ce7-82e8-129ab88f150c': 'session_0b59d118-8d04-4382-af1f-8f2d997f7e2e',
    'remember_web_3dc7a913ef5fd4b890ecabe3487085573e16cf82': 'eyJpdiI6IjJoZmpYWjFYOENjQjQ1Lyt2TVpNSEE9PSIsInZhbHVlIjoiRkRCSkJwcXpvZG12MTNiWmhZOTU0cmdqQU9rUGgrQUw5V3dkU01HTENlK3lYdmJHYkVibldxWDJENmNlK2w1QzJHSStTdzdHVzhYYXE2UFUwdnEwRTZGVzQwUUxrKzErMHoyRTdreC9ra3NDL29lNkVSaWRVanZIVFNBTmZwamJOU2RmRGJtbG1FYWdoVnJ6M0RKV3pnR2s1SkhJUW9mQUtJQmdFRSsxZWdISWNHNnRnNFlLcVkwbnJwTXNYY2xCZ1h3ak9MeDV4MGZPUHVJUmJwNGlDYng5YmNOekxlUFcwTElLdEFKWjJkdz0iLCJtYWMiOiJiYjRjYjdkNWI2MzQ0NTY0Y2Q1Y2FkZDAyYTc3NGVjNDMxZWZjNzZjZjVkZGQwMzllODBkYjUzODE1MmRhOTZjIiwidGFnIjoiIn0%3D'
    }


session.headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:95.0) Gecko/20100101 Firefox/95.0',
    'Accept': 'text/html, application/xhtml+xml',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'X-Requested-With': 'XMLHttpRequest',
    'X-Inertia': 'true',
    'X-Inertia-Version': 'eaab6f8db0b109568ae5e7468dbd534a',
    'X-XSRF-TOKEN': 'eyJpdiI6IitnM3BydE1nMk9ZeUh5U2g2U29RaFE9PSIsInZhbHVlIjoiQVBoUWRnem9HU1g3S1JMK3ZSNWZ6V0greEN2TVlFRmF1YVJWZW9NcFVWd1RTY3hKVzBKUVVRSnU1ZlZnT0Y5bFpRQy9IU1BGci91eG1ZM0dOcjd5Qk1oWG0rMzdsckFQR29oeXpHSlo1SjJqcE9hSjJzOUtmZ0pkRzRFb0NHSkIiLCJtYWMiOiI2MTI2MzNiNGMzNjNlODUwMjdiYWM1NGY0ZWI1ZDMyMDliNjg2NTEyNTEyNDMxYTViN2IyMTc1M2UzOWE5ZTZhIiwidGFnIjoiIn0=',
    'Referer': 'https://mymoneyja.com/login',
    'Connection': 'keep-alive',
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



# x = coll.insert_one(documents[0])
# x = col.insert_many(documents)
# print(x)
