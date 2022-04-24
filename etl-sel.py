
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
session = requests.Session()

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



def initailize_scraper():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu-sandbox')
    options.add_argument("--single-process")
    options.add_argument('window-size=1920x1080')
    options.add_argument(
        '"user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"')

    page_to_scrape= webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    page_to_scrape.get("https://mymoneyja.com/login")
    
    email = page_to_scrape.find_element(By.NAME, "email")
    password = page_to_scrape.find_element(By.NAME, "password")
    email.send_keys(os.environ.get("EMAIL"))
    password.send_keys(os.environ.get("PASSWORD"))

    page_to_scrape.find_element(By.CSS_SELECTOR, "body > div > div > form > div:nth-child(4) > button").click()
    time.sleep(3)
    page_to_scrape.find_element(By.CSS_SELECTOR, "a.w-full:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3)").click()
    time.sleep(3)
    selCookies = page_to_scrape.get_cookies()
   
    #store the headers in the session
    for request in page_to_scrape.requests:
        if request.headers['x-xsrf-token']:
            del session.headers['Referer'] 
            del session.headers['X-XSRF-TOKEN'] 
            del session.headers['User-Agent'] 
            del session.headers['X-Inertia-Version'] 
            session.headers['Referer'] = request.headers['referer']
            session.headers['X-XSRF-TOKEN'] = request.headers['x-xsrf-token']
            session.headers['User-Agent'] = request.headers['user-agent']
            session.headers['X-Inertia-Version'] = request.headers['x-inertia-version']
            
            
    #store the cookies in the session
    for cookie in selCookies:
        session.cookies[cookie["name"]] = cookie["value"]

    time.sleep(5)


def gen_company_list():
    response = session.get("https://mymoneyja.com/stock/138SL")

    # get scaped data for tickers
    stock_data = json.loads(response.content)


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
    response2 = session.get(
        f"https://mymoneyja.com/stock/{company}",
       
    )
    soup = BeautifulSoup(response2.content, "html.parser")
    stock_data = json.loads(soup.text)
    key = {}
   
    key["name"] = stock_data["props"]["company"]["name"]
    key["ticker"] = stock_data["props"]["company"]["ticker"]
    key["blurb"] = stock_data["props"]["company"]["blurb"]
  
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
    gen_company_list()
    with ThreadPoolExecutor() as executor:
        executor.map(get_data, companies)
    # store_mongo()
    # store_dynamo(documents)
    
    s3object = s3.Object(os.environ.get("S3_BUCKET"), f'jsonv3/companies_list.json')
    response = s3object.put( Body=(bytes(json.dumps(companies_list).encode('UTF-8'))), ContentType='application/json' )
scraper("event", "context")