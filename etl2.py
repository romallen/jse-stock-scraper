from pymongo.message import _first_batch
import requests
from bs4 import BeautifulSoup
import json
from dotenv import load_dotenv
import os
from requests.sessions import Request
import pymongo
import boto3
import re

load_dotenv()
s3 = boto3.resource('s3')

session = requests.Session()

companies = [
            [ '138SL', '138 STUDENT LIVING JAMAICA LIMITED' ],
            [ '1834', '1834 INVESTMENTS LIMITED' ],
            [ 'AFS', 'ACCESS FINANCIAL SERVICES LIMITED' ],
            [ 'AMG', 'AMG PACKAGING  & PAPER COMPANY LIMITED' ],
            [ 'BIL', 'BARITA INVESTMENTS LIMITED' ],
            [ 'BPOW', 'BLUE POWER GROUP LIMITED' ],
            [ 'BRG', 'BERGER PAINTS JAMAICA LTD.' ],
            [ 'CABROKERS', 'CARIBBBEAN ASSURANCE BROKERS LIMITED' ],
            [ 'CAC', 'CAC 2000 LIMITED' ],
            [ 'CAR', 'CARRERAS LIMITED' ],
            [ 'CBNY', 'CIBONEY GROUP LIMITED' ],
            [ 'CCC', 'CARIBBEAN CEMENT COMPANY LTD' ],
            [ 'CFF', 'CARIBBEAN FLAVOURS & FRAGRANCES LIMITED' ],
            [ 'CHL', 'CARGO HANDLERS LIMITED' ],
            [ 'CPFV', 'EPPLEY CARIBBEAN PROPERTY FUND LIMITED SCC' ],
            [ 'CPJ', 'CARIBBEAN PRODUCERS JAMAICA LIMITED' ],
            [ 'DCOVE', 'DOLPHIN COVE LIMITED' ],
            [ 'DTL', 'DERRIMON TRADING COMPANY LIMITED' ],
            [ 'ECL', 'EXPRESS CATERING LIMITED' ],
            [ 'EFRESH', 'EVERYTHING FRESH LIMITED' ],
            [ 'ELITE', 'ELITE DIAGNOSTIC LIMITED' ],
            [ 'EPLY', 'EPPLEY LIMITED' ],
            [ 'FIRSTROCKJMD', 'FIRST ROCK CAPITAL HOLDINGS LIMITED' ],
            [ 'FIRSTROCKUSD', 'FIRST ROCK CAPITAL HOLDINGS LIMITED  (USD)' ],
            [ 'FOSRICH', 'FOSRICH COMPANY LIMITED' ],
            [ 'FTNA', 'FONTANA LIMITED' ],
            [ 'GENAC', 'GENERAL ACCIDENT INSURANCE COMPANY (JA) LIMITED' ],
            [ 'GHL', 'GUARDIAN HOLDINGS LIMITED' ],
            [ 'GK', 'GRACEKENNEDY LIMITED' ],
            [ 'GWEST', 'GWEST CORPORATION LIMITED ORDINARY SHARES' ],
            [ 'HONBUN', 'HONEY BUN (1982) LIMITED' ],
            [ 'ICREATE', 'ICREATE LIMITED ORDINARY SHARES' ],
            [ 'INDIES', 'INDIES PHARMA JAMAICA LIMITED ORDINARY SHARES' ],
            [ 'ISP', 'ISP FINANCE SERVICES LIMITED' ],
            [ 'JAMT', 'JAMAICAN TEAS LIMITED' ],
            [ 'JBG', 'JAMAICA BROILERS GROUP' ],
            [ 'JETCON', 'JETCON CORPORATION LIMITED' ],
            [ 'JMMBGL', 'JMMB GROUP LIMITED' ],
            [ 'JP', 'JAMAICA PRODUCERS GROUP LTD.' ],
            [ 'JSE', 'JAMAICA STOCK EXCHANGE' ],
            [ 'KEX', 'KNUTSFORD EXPRESS SERVICES LIMITED' ],
            [ 'KEY', 'KEY INSURANCE COMPANY LIMITED' ],
            [ 'KLE', 'K.L.E. GROUP LIMITED' ],
            [ 'KPREIT', 'KINGSTON PROPERTIES LIMITED' ],
            [ 'KREMI', 'CARIBBEAN CREAM LIMITED' ],
            [ 'KW', 'KINGSTON WHARVES LIMITED' ],
            [ 'LAB', 'THE LIMNERS AND BARDS LIMITED' ],
            [ 'LASD', 'LASCO DISTRIBUTORS LIMITED' ],
            [ 'LASF', 'LASCO FINANCIAL SERVICES LIMITED' ],
            [ 'LASM', 'LASCO MANUFACTURING LIMITED' ],
            [ 'LUMBER', 'LUMBER DEPOT LIMITED' ],
            [ 'MAILPAC', 'MAILPAC GROUP LIMITED' ],
            [ 'MDS', 'MEDICAL DISPOSABLES & SUPPLIES LIMITED' ],
            [ 'MEEG', 'MAIN EVENT ENTERTAINMENT GROUP' ],
            [ 'MIL', 'MAYBERRY INVESTMENTS LIMITED' ],
            [ 'MJE', 'MAYBERRY JAMAICAN EQUITIES LIMITED' ],
            [ 'MPCCEL', 'MPC CARIBBEAN CLEAN ENERGY LIMITED' ],
            [ 'MPCCELUSD', 'MPC CARIBBEAN CLEAN ENERGY LIMITED USD' ],
            [ 'MTL', 'MARGARITAVILLE (TURKS) LIMITED' ],
            [ 'MTLUSD', 'MARGARITAVILLE (TURKS) LIMITED USD' ],
            [ 'NCBFG', 'NCB FINANCIAL GROUP LIMITED ' ],
            [ 'PAL', 'PALACE AMUSEMENT CO. LTD.' ],
            [ 'PBS', 'PRODUCTIVE BUSINESS SOLUTION LTD USD ORDINARY SHARES' ],
            [ 'PJAM', 'PANJAM INVESTMENT LIMITED' ],
            [ 'PJX', 'PORTLAND JSX LIMITED' ],
            [ 'PROVEN', 'PROVEN INVESTMENTS LIMITED JMD' ],
            [ 'PROVENUSD', 'PROVEN INVESTMENTS LIMITED USD' ],
            [ 'PTL', 'PARAMOUNT TRADING (JAMAICA) LIMITED' ],
            [ 'PULS', 'PULSE INVESTMENTS LIMITED' ],
            [ 'PURITY', 'CONSOLIDATED BAKERIES (JAMAICA) LIMITED' ],
            [ 'QWI', 'QWI INVESTMENTS LIMITED' ],
            [ 'RJR', 'RADIO JAMAICA LIMITED' ],
            [ 'ROC', 'IRONROCK INSURANCE COMPANY LIMITED' ],
            [ 'SALF', 'SALADA FOODS JAMAICA LTD.' ],
            [ 'SCIJMD', 'SYGNUS CREDIT INVESTMENTS LIMITED JMD ORDINARY SHARES' ],
            [ 'SCIJMD', 'SYGNUS CREDIT INVESTMENTS LIMITED USD ORDINARY SHARES' ],
            [ 'SCIUSD', 'SYGNUS CREDIT INVESTMENTS LIMITED JMD ORDINARY SHARES' ],
            [ 'SCIUSD', 'SYGNUS CREDIT INVESTMENTS LIMITED USD ORDINARY SHARES' ],
            [ 'SELECTF', 'SAGICOR SELECT FUNDS LIMITED FINANCIAL' ],
            [
              'SELECTMD',
              'SAGICOR SELECT FUNDS LIMITED MANUFACTURING & DISTRIBUTION'
            ],
            [ 'SEP', 'SEPROD LIMITED' ],
            [ 'SGJ', 'SCOTIA GROUP JAMAICA LIMITED' ],
            [ 'SIL', 'STERLING INVESTMENTS LIMITED' ],
            [ 'SILUSD', 'STERLING INVESTMENTS LIMITED USD' ],
            [ 'SJ', 'SAGICOR GROUP JAMAICA LIMITED' ],
            [ 'SML', 'STANLEY MOTTA LIMITED ORDINARY SHARES' ],
            [ 'SOS', 'STATIONERY AND OFFICE SUPPLIES LIMITED' ],
            [ 'SRFJMD', 'SYGNUS REAL ESTATE FINANCE LIMITED' ],
            [ 'SRFUSD', 'SYGNUS REAL ESTATE FINANCE LIMITED' ],
            [ 'SSLVC', 'SSL VENTURE CAPITAL JAMAICA LIMITED' ],
            [ 'SVL', 'SUPREME VENTURES LIMITED' ],
            [ 'TJH', 'TRANSJAMAICAN HIGHWAY LIMITED JMD' ],
            [ 'TJHUSD', 'TRANSJAMAICAN HIGHWAY LIMITED USD' ],
            [ 'TROPICAL', 'TROPICAL BATTERY' ],
            [ 'TTECH', 'TTECH LIMITED' ],
            [ 'VMIL', 'VICTORIA MUTUAL INVESTMENTS LTD ORDINARY SHARES' ],
            [ 'WIG', 'WIGTON WINDFARM LIMITED ORDINARY SHARES' ],
            [ 'WISYNCO', 'WISYNCO GROUP LTD ORDINARY SHARES' ],
            [ 'XFUND', 'SAGICOR REAL ESTATE X FUND LTD.' ]
            ];  

    


documents = []

# populates dictionary with trade data
def get_data(company):
    #keystr = list(dictionary.keys())
    #keystr = keystr[0]
    print(company)
    response2 = session.get(
        "https://www.jamstockex.com/market-data/instruments/?symbol={0}".format(company),
        # cookies=cookies,
        # headers=session.headers,
    )
    soup = BeautifulSoup(response2.content, "html.parser")
    print(soup.find_all(text= re.compile('data: '),limit=1 ))
    # stock_data = json.loads(soup.text)
    # key = {}
   
    # key["name"] = stock_data["props"]["company"]["name"]
    # key["ticker"] = stock_data["props"]["company"]["ticker"]
    # key["blurb"] = stock_data["props"]["company"]["blurb"]
    # #key["close_prices"] = stock_data["props"]["company"]["data"]["close_prices"]
    # key["ohlc"] = stock_data["props"]["company"]["data"]["ohlc"]
    # key["volume"] = stock_data["props"]["company"]["data"]["volume"]
    # documents.append(key)
    
    # stockChartData = []
    # stockChartData.append([key["name"], key["ticker"], key["blurb"]])
    # for i in range(len(stock_data["props"]["company"]["data"]["ohlc"])):
    #     price = key["ohlc"][i]
    #     vol = key["volume"][i]["volume"]
    #     price.append(vol)
    #     stockChartData.append(price)
    
    # s3object = s3.Object('romallen.com', f'json/{company}-data.json')
    # s3object.put( Body=(bytes(json.dumps(stockChartData).encode('UTF-8'))), ContentType='application/json' )



for company in companies:
    get_data(company[0])


# uploads dictionaries as a collection to MongoDb
client = pymongo.MongoClient(os.environ.get("DB_URL"))
db = client["jse"]
coll = db["companies"]

# x = coll.delete_many({})
# print(x.deleted_count, " documents deleted.")
#y = coll.insert_many(documents)
print(y)

