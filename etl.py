
from asyncio.log import logger
from decimal import Decimal
import shutil
import requests
from bs4 import BeautifulSoup
import json
from dotenv import load_dotenv
import os
from requests.sessions import Request
import pymongo
import boto3
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
import time
from concurrent.futures import ThreadPoolExecutor
from tempfile import mkdtemp


load_dotenv()
s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')
s = requests.Session()


def initailize_scraper():
    link = 'https://mymoneyja.com/login'
   
    s.headers = {
        
    'authority': 'mymoneyja.com',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
    'dnt': '1',
    'x-xsrf-token': 'eyJpdiI6ImtNeVhIUmdCSXk0ZVhHNXMyUlg3QWc9PSIsInZhbHVlIjoiWkN0ZnpRSFluWnppaG0wL3I3OWFzSW5ORGJjZ01PQUhWbnhiYS91YVA3T09WWGpxdUtkN0l4MEhJbTRFejJ1Ni9YTW43S1kxZU5tM3QySld6aU8vZHdnTXBZbVBMaXJnbkJNZE5TRFRkUTI2VnhtVTQwQVFqS2pzcFRwMnJFRlIiLCJtYWMiOiJkYWRjZTVkZWE2NGNiNDFiMTI2NjVlMTZjYzRjMDg2MmQ0YzI5ZDY1YjgzMjAyNThiZDc5NDFjZWVmZDgwY2JhIiwidGFnIjoiIn0=',
    'sec-ch-ua-mobile': '?0',
    'x-inertia': 'true',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
    'accept': 'text/html, application/xhtml+xml',
    'x-inertia-version': 'a59a317717f2ba44709a28d4b9409b68',
    'x-requested-with': 'XMLHttpRequest',
    'sec-ch-ua-platform': '"macOS"',
    'origin': 'https://mymoneyja.com',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://mymoneyja.com/login',
    'accept-language': 'en-US,en;q=0.9,ja;q=0.8,fr;q=0.7',
    'cookie': 'crisp-client%2Fsession%2F595850e5-08f3-4ce7-82e8-129ab88f150c=session_4bd66089-a4f5-45a4-a096-045e8cbe2cb0; XSRF-TOKEN=eyJpdiI6ImtNeVhIUmdCSXk0ZVhHNXMyUlg3QWc9PSIsInZhbHVlIjoiWkN0ZnpRSFluWnppaG0wL3I3OWFzSW5ORGJjZ01PQUhWbnhiYS91YVA3T09WWGpxdUtkN0l4MEhJbTRFejJ1Ni9YTW43S1kxZU5tM3QySld6aU8vZHdnTXBZbVBMaXJnbkJNZE5TRFRkUTI2VnhtVTQwQVFqS2pzcFRwMnJFRlIiLCJtYWMiOiJkYWRjZTVkZWE2NGNiNDFiMTI2NjVlMTZjYzRjMDg2MmQ0YzI5ZDY1YjgzMjAyNThiZDc5NDFjZWVmZDgwY2JhIiwidGFnIjoiIn0%3D; mymoneyja_session=eyJpdiI6ImRXcm1yanpNOHVoYUxWVTBGNnd0dVE9PSIsInZhbHVlIjoiWjcxcTRmZVFYWWhJTGtjY1RBanNMUkVISUczZnA4ay9hU3hYOGhGbXVadjZ1T2d5dUF3MXJzZTZHUzdjOEZlQWlLbHZ6dXdLamRsL3FFdXJaVWVTZUErWEtiWWRpcjJrZEZyL3hJUWpzUHYwL2UzdDFHSE5oZHdveWtPZ1lXSk0iLCJtYWMiOiI4ZGE0YmMxZTllMDI3NDMzNjE5NDRlZDc2YzBiNTE5OTEwZDYwZTAxNWU5MjFiZTA1N2RlZGRmMDc5YWRmMGQ4IiwidGFnIjoiIn0%3D',

 
    }
    
    res = s.get(link)
    # print(s.cookies.get_dict().keys())
    s.headers['x-xsrf-token'] = s.cookies.get_dict()['XSRF-TOKEN']
    
    cook = ""
    
    for key, value in s.cookies.get_dict().items():
        cook += key + "=" + value + ";"
    
    s.headers['cookie'] = cook
  
    # print(s.headers)
    json_data = {
    'email': 'romallen1@gmail.com',
    'password': 'En1gm@t1c',
    'remember': None,
    }

    # 'https://mymoneyja.com/login', headers=headers, json=json_data)
    p = s.post(link, json=json_data)
    print(p)
    
    response = s.get('https://mymoneyja.com/market')
    print(response.text)
  
def gen_company_list():
    response = s.get("https://mymoneyja.com/stock/138SL")

    # get scaped data for tickers
    stock_data = json.loads(response.content)
    print(stock_data)

    # saves the companies tickers in a dictionary
    for comp in stock_data["props"]["companies"]:
        companies.append(comp["ticker"])
        
    companies_list["companies"] =  stock_data["props"]["companies"]


companies = ["138SL"]
documents = []
companies_list = {}
# populates dictionary with trade data
def get_data(company):
    print("Scraping: " + company)
    response2 = s.get(
        f"https://mymoneyja.com/stock/{company}",
       
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
    
    key["next_report"] = stock_data["props"]["company"]["next_report"]
    key["metrics"] = stock_data["props"]["company"]["metrics"]
    key["corporate_actions"] = stock_data["props"]["company"]["corporate_actions"]
    key["financials"] = stock_data["props"]["company"]["data"]["financial"]
    key["news"] = stock_data["props"]["news"]
    key["financialReports"] = stock_data["props"]["financialReports"]
    stockChartData = []
    # stockChartData.append([key["name"], key["ticker"], key["blurb"]])
    for i in range(len(stock_data["props"]["company"]["data"]["ohlc"])):
        price = key["ohlc"][i]
        vol = key["volume"][i]["volume"]
        price.append(vol)
        stockChartData.append(price)
    key["ohlcv"]= stockChartData
    # stockChartData.append([key["next_report"], key["metrics"], key["corporate_actions"], key["financials"], key["news"], key["financialReports"]])

    documents.append(key)
    del key["ohlc"]
    del key["volume"]
    try :
        s3object = s3.Object(os.environ.get("S3_BUCKET"), f'jsonv3/{company}.json')
        response = s3object.put( Body=(bytes(json.dumps(key).encode('UTF-8'))), ContentType='application/json' )
        print(response)

    except Exception as e:
        print("error: " + str(e))
        



def store_mongo():
    # uploads documents to MongoDb
    client = pymongo.MongoClient(os.environ.get("DB_URL"),  )
    db = client["jse"]
    coll = db["companies"]

    x= coll.delete_many({})
    print(x)
    y = coll.insert_many(documents)
    #y = coll.update_many({}, {'$set': {'data': documents}}, upsert=True)
    print(y)
    z =coll.update_one({"name": "meta"}, {"$set": {"last_updated": int(time.time())*1000, "companies": companies}}, upsert=True)
    print(z)
    
    
def store_dynamo(companyDocuments):
    table = dynamodb.Table('jse')
    
    companies =json.loads(json.dumps(companyDocuments), parse_float=Decimal)

    for doc in companies:
        ticker = doc["ticker"]
        print("Storing: ", ticker) 
        table.put_item(Item=doc)
  
    

def scraper(event, context): 
    initailize_scraper()
    # gen_company_list()
    # with ThreadPoolExecutor() as executor:
    #     executor.map(get_data, companies)
    # store_mongo()
    # store_dynamo(documents)
    
    # s3object = s3.Object(os.environ.get("S3_BUCKET"), f'jsonv3/companies_list.json')
    # response = s3object.put( Body=(bytes(json.dumps(companies_list).encode('UTF-8'))), ContentType='application/json' )
scraper("event", "context")