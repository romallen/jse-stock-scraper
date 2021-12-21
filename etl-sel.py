from pymongo.message import _first_batch
import requests
from bs4 import BeautifulSoup
import json
from dotenv import load_dotenv
import os
from requests.sessions import Request
import pymongo
import boto3
from selenium.webdriver.chrome.service import Service
#from selenium import webdriver
from selenium.webdriver.common.by import By
from seleniumwire import webdriver
import time
load_dotenv()
s3 = boto3.resource('s3')

session = requests.Session()
# session.cookies ={'XSRF-TOKEN': '',
#                   'mymoneyja_session': ''
#                   }
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


browser_driver = Service('/usr/local/bin/chromedriver')
page_to_scrape = webdriver.Chrome(service=browser_driver)
page_to_scrape.get("https://mymoneyja.com/login")
email = page_to_scrape.find_element(By.NAME, "email")
password = page_to_scrape.find_element(By.NAME, "password")
email.send_keys(os.environ.get("EMAIL"))
password.send_keys(os.environ.get("PASSWORD"))

page_to_scrape.find_element(By.CSS_SELECTOR, "body > div > div > form > div:nth-child(4) > button").click()

selCookies = page_to_scrape.get_cookies()

for request in page_to_scrape.requests:
    if request.headers['x-xsrf-token']:
        session.headers['Referer'] = request.headers['referer']
        session.headers['X-XSRF-TOKEN'] = request.headers['x-xsrf-token']
        session.headers['User-Agent'] = request.headers['user-agent']
        session.headers['X-Inertia-Version'] = request.headers['x-inertia-version']
        
        

for cookie in selCookies:
    session.cookies[cookie["name"]] = cookie["value"]
print(session.cookies)
    
#print(session.headers)




time.sleep(10)

response = session.get(
    "https://mymoneyja.com/stock/138SL", 
)
print(response.content)
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



#for dictionary in dictionaries:
    #get_data(dictionary)


# uploads dictionaries as a collection to MongoDb
client = pymongo.MongoClient(os.environ.get("DB_URL"))
db = client["jse"]
coll = db["companies"]

# x = coll.delete_many({})
# print(x.deleted_count, " documents deleted.")
y = coll.insert_many(documents)
print(y)

