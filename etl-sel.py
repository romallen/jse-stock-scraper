import requests
from bs4 import BeautifulSoup
import json
from dotenv import load_dotenv
import os
import pymongo
import boto3
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
import time
from concurrent.futures import ThreadPoolExecutor



load_dotenv()
s3 = boto3.resource('s3')
# dynamodb = boto3.resource('dynamodb')
session = requests.Session()

session.headers = {
       
        'authority': 'mymoneyja.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-US,en;q=0.9,ja;q=0.8,fr;q=0.7',
        'dnt': '1',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36',
    }

def initailize_scraper():

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu-sandbox')
    options.add_argument("--single-process")
  
    options.add_argument(
        '"user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"')
    
    page_to_scrape= webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    page_to_scrape.implicitly_wait(10)
    page_to_scrape.get("https://mymoneyja.com/login")
    
    email = page_to_scrape.find_element(By.NAME, "email")
    password = page_to_scrape.find_element(By.NAME, "password")
    email.send_keys(os.environ.get("EMAIL"))
    password.send_keys(os.environ.get("PASSWORD"))

    page_to_scrape.find_element(By.CSS_SELECTOR, "body > div > div > form > div:nth-child(4) > button").click()
    time.sleep(3)
    # page_to_scrape.find_element(By.CSS_SELECTOR, "a.w-full:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3)").click()
    # time.sleep(3)
    selCookies = page_to_scrape.get_cookies()
    #store the headers in the session
    # for request in page_to_scrape.requests:
    #     if request.headers['x-xsrf-token']:
    #         print("starting scraper",  request)
            # session.headers.update(request.headers)
            # del session.headers['Referer'] 
            # del session.headers['X-XSRF-TOKEN'] 
            # del session.headers['User-Agent'] 
            # del session.headers['X-Inertia-Version'] 
            # session.headers['Referer'] = request.headers['referer']
            # session.headers['X-XSRF-TOKEN'] = request.headers['x-xsrf-token']
            # session.headers['User-Agent'] = request.headers['user-agent']
            # session.headers['X-Inertia-Version'] = request.headers['x-inertia-version']
            
            
    #store the cookies in the session
    for cookie in selCookies:
        session.cookies[cookie["name"]] = cookie["value"]
    time.sleep(5)


def gen_company_list():
    response = session.get("https://mymoneyja.com/stock/138SL")
    comp_list_soup = BeautifulSoup(response.content, "html.parser")
    comp_data =comp_list_soup.find("div", {"id": "app"})
    # get scaped data for tickers
    stock_data = json.loads(comp_data.attrs["data-page"])


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
    comp_data = soup.find("div", {"id": "app"})
    # get scaped data for tickers
    stock_data = json.loads(comp_data.attrs["data-page"])
    # stock_data = json.loads(soup.text)
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
    
    
# def store_dynamo(companyDocuments):
#     table = dynamodb.Table('jse')
    
#     companies =json.loads(json.dumps(companyDocuments), parse_float=Decimal)

#     for doc in companies:
#         ticker = doc["ticker"]
#         print("Storing: ", ticker) 
#         table.put_item(Item=doc)
  
    

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