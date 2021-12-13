# import requests
# import json
# import pymongo
# import os
# from dotenv import load_dotenv
   
try:
    import json
    from flask import Flask, render_template,make_response
    import requests
    
    print("ALl modules Loaded ")
except Exception as e:
    print("Error : {} ".format(e))

app = Flask(__name__)

# uri = os.environ.get("DB_URL") or os.environ.get("MONGODB_URI")
# load_dotenv()


url = "https://data.mongodb-api.com/app/data-udhoo/endpoint/data/beta/action/findOne"
payload = json.dumps(
    {
        "collection": "companies",
        "database": "jse",
        "dataSource": "Cluster0",
        #"projection": {"_id": 1, "name": 1}, 
        "filter": {"ticker": "LAB"},
    }
)
headers = {
    "Content-Type": "application/json",
    "Access-Control-Request-Headers": "*",
    "api-key": "ueM6pG5gVMmnAJZPMgQS649GV8JEQtl7eGL0fHrqyq3LEJJatYp9hskCDRq5wmAa",
}
response = requests.request("POST", url, headers=headers, data=payload)

rawData = json.loads(response.text)["document"]
ohlcv = []

for i in range(len(rawData["ohlc"])):
    price = rawData["ohlc"][i]
    vol = rawData["volume"][i]["volume"]
    price.append(vol)


    ohlcv.append(price) 
    
#print(json.dumps(ohlcv))





@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/pipe', methods=["GET", "POST"])
def pipe():
    # payload = {}
    # headers = {}
    # url = "https://demo-live-data.highcharts.com/aapl-ohlcv.json"
    # r = requests.get(url, headers=headers, data ={})
    # r = r.json()
    # return {"res":r}
    return {"res":ohlcv}


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)

# {
# 	"companies": [
# 		{
# 			"id": 1,
# 			"name": "138 STUDENT LIVING JAMAICA LIMITED",
# 			"ticker": "138SL",
# 			"industry": "OTHER",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "main"
# 		},
# 		{
# 			"id": 3,
# 			"name": "1834 INVESTMENTS LIMITED",
# 			"ticker": "1834",
# 			"industry": "COMMUNICATIONS",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "main"
# 		},
# 		{
# 			"id": 67,
# 			"name": "ACCESS FINANCIAL SERVICES LIMITED",
# 			"ticker": "AFS",
# 			"industry": "FINANCE",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "junior"
# 		},
# 		{
# 			"id": 68,
# 			"name": "AMG PACKAGING  & PAPER COMPANY LIMITED",
# 			"ticker": "AMG",
# 			"industry": "MANUFACTURING",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "junior"
# 		},
# 		{
# 			"id": 4,
# 			"name": "BARITA INVESTMENTS LIMITED",
# 			"ticker": "BIL",
# 			"industry": "FINANCE",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "main"
# 		},
# 		{
# 			"id": 69,
# 			"name": "BLUE POWER GROUP LIMITED",
# 			"ticker": "BPOW",
# 			"industry": "MANUFACTURING",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "junior"
# 		},
# 		{
# 			"id": 5,
# 			"name": "BERGER PAINTS JAMAICA LTD.",
# 			"ticker": "BRG",
# 			"industry": "MANUFACTURING",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "main"
# 		},
# 		{
# 			"id": 74,
# 			"name": "CARIBBBEAN ASSURANCE BROKERS LIMITED",
# 			"ticker": "CABROKERS",
# 			"industry": "INSURANCE",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "junior"
# 		},
# 		{
# 			"id": 72,
# 			"name": "CAC 2000 LIMITED",
# 			"ticker": "CAC",
# 			"industry": "RETAIL",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "junior"
# 		},
# 		{
# 			"id": 8,
# 			"name": "CARRERAS LIMITED",
# 			"ticker": "CAR",
# 			"industry": "RETAIL",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "main"
# 		},
# 		{
# 			"id": 9,
# 			"name": "CIBONEY GROUP LIMITED",
# 			"ticker": "CBNY",
# 			"industry": "TOURISM",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "main"
# 		},
# 		{
# 			"id": 7,
# 			"name": "CARIBBEAN CEMENT COMPANY LTD",
# 			"ticker": "CCC",
# 			"industry": "MANUFACTURING",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "main"
# 		},
# 		{
# 			"id": 76,
# 			"name": "CARIBBEAN FLAVOURS & FRAGRANCES LIMITED",
# 			"ticker": "CFF",
# 			"industry": "MANUFACTURING",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "junior"
# 		},
# 		{
# 			"id": 73,
# 			"name": "CARGO HANDLERS LIMITED",
# 			"ticker": "CHL",
# 			"industry": "OTHER",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "junior"
# 		},
# 		{
# 			"id": 11,
# 			"name": "EPPLEY CARIBBEAN PROPERTY FUND LIMITED SCC",
# 			"ticker": "CPFV",
# 			"industry": "FINANCE",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "main"
# 		},
# 		{
# 			"id": 77,
# 			"name": "CARIBBEAN PRODUCERS JAMAICA LIMITED",
# 			"ticker": "CPJ",
# 			"industry": "RETAIL",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "main"
# 		},
# 		{
# 			"id": 81,
# 			"name": "DOLPHIN COVE LIMITED",
# 			"ticker": "DCOVE",
# 			"industry": "TOURISM",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "junior"
# 		},
# 		{
# 			"id": 79,
# 			"name": "DERRIMON TRADING COMPANY LIMITED",
# 			"ticker": "DTL",
# 			"industry": "RETAIL",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "junior"
# 		},
# 		{
# 			"id": 84,
# 			"name": "EXPRESS CATERING LIMITED",
# 			"ticker": "ECL",
# 			"industry": "OTHER",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "junior"
# 		},
# 		{
# 			"id": 83,
# 			"name": "EVERYTHING FRESH LIMITED",
# 			"ticker": "EFRESH",
# 			"industry": "OTHER",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "junior"
# 		},
# 		{
# 			"id": 82,
# 			"name": "ELITE DIAGNOSTIC LIMITED",
# 			"ticker": "ELITE",
# 			"industry": "OTHER",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "junior"
# 		},
# 		{
# 			"id": 12,
# 			"name": "EPPLEY LIMITED",
# 			"ticker": "EPLY",
# 			"industry": "FINANCE",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "main"
# 		},
# 		{
# 			"id": 15,
# 			"name": "FIRST ROCK CAPITAL HOLDINGS LIMITED",
# 			"ticker": "FIRSTROCKJMD",
# 			"industry": "OTHER",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "main"
# 		},
# 		{
# 			"id": 116,
# 			"name": "FIRST ROCK CAPITAL HOLDINGS LIMITED  (USD)",
# 			"ticker": "FIRSTROCKUSD",
# 			"industry": "OTHER",
# 			"type": "ORDINARY",
# 			"currency": "USD",
# 			"market": "usd"
# 		},
# 		{
# 			"id": 87,
# 			"name": "FOSRICH COMPANY LIMITED",
# 			"ticker": "FOSRICH",
# 			"industry": "OTHER",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "junior"
# 		},
# 		{
# 			"id": 85,
# 			"name": "FONTANA LIMITED",
# 			"ticker": "FTNA",
# 			"industry": "OTHER",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "junior"
# 		},
# 		{
# 			"id": 88,
# 			"name": "GENERAL ACCIDENT INSURANCE COMPANY (JA) LIMITED",
# 			"ticker": "GENAC",
# 			"industry": "INSURANCE",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "junior"
# 		},
# 		{
# 			"id": 147,
# 			"name": "GUARDIAN HOLDINGS LIMITED",
# 			"ticker": "GHL",
# 			"industry": "FINANCE",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "main"
# 		},
# 		{
# 			"id": 16,
# 			"name": "GRACEKENNEDY LIMITED",
# 			"ticker": "GK",
# 			"industry": "CONGLOMERATES",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "main"
# 		},
# 		{
# 			"id": 89,
# 			"name": "GWEST CORPORATION LIMITED ORDINARY SHARES",
# 			"ticker": "GWEST",
# 			"industry": "OTHER",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "junior"
# 		},
# 		{
# 			"id": 90,
# 			"name": "HONEY BUN (1982) LIMITED",
# 			"ticker": "HONBUN",
# 			"industry": "MANUFACTURING",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "junior"
# 		},
# 		{
# 			"id": 91,
# 			"name": "ICREATE LIMITED ORDINARY SHARES",
# 			"ticker": "ICREATE",
# 			"industry": "OTHER",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "junior"
# 		},
# 		{
# 			"id": 92,
# 			"name": "INDIES PHARMA JAMAICA LIMITED ORDINARY SHARES",
# 			"ticker": "INDIES",
# 			"industry": "RETAIL",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "junior"
# 		},
# 		{
# 			"id": 94,
# 			"name": "ISP FINANCE SERVICES LIMITED",
# 			"ticker": "ISP",
# 			"industry": "FINANCE",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "junior"
# 		},
# 		{
# 			"id": 95,
# 			"name": "JAMAICAN TEAS LIMITED",
# 			"ticker": "JAMT",
# 			"industry": "MANUFACTURING",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "junior"
# 		},
# 		{
# 			"id": 17,
# 			"name": "JAMAICA BROILERS GROUP",
# 			"ticker": "JBG",
# 			"industry": "MANUFACTURING",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "main"
# 		},
# 		{
# 			"id": 96,
# 			"name": "JETCON CORPORATION LIMITED",
# 			"ticker": "JETCON",
# 			"industry": "RETAIL",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "junior"
# 		},
# 		{
# 			"id": 31,
# 			"name": "JMMB GROUP LIMITED",
# 			"ticker": "JMMBGL",
# 			"industry": "FINANCE",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "main"
# 		},
# 		{
# 			"id": 18,
# 			"name": "JAMAICA PRODUCERS GROUP LTD.",
# 			"ticker": "JP",
# 			"industry": "CONGLOMERATES",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "main"
# 		},
# 		{
# 			"id": 25,
# 			"name": "JAMAICA STOCK EXCHANGE",
# 			"ticker": "JSE",
# 			"industry": "FINANCE",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "main"
# 		},
# 		{
# 			"id": 98,
# 			"name": "KNUTSFORD EXPRESS SERVICES LIMITED",
# 			"ticker": "KEX",
# 			"industry": "OTHER",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "junior"
# 		},
# 		{
# 			"id": 34,
# 			"name": "KEY INSURANCE COMPANY LIMITED",
# 			"ticker": "KEY",
# 			"industry": "INSURANCE",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "main"
# 		},
# 		{
# 			"id": 97,
# 			"name": "K.L.E. GROUP LIMITED",
# 			"ticker": "KLE",
# 			"industry": "OTHER",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "junior"
# 		},
# 		{
# 			"id": 35,
# 			"name": "KINGSTON PROPERTIES LIMITED",
# 			"ticker": "KPREIT",
# 			"industry": "OTHER",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "main"
# 		},
# 		{
# 			"id": 75,
# 			"name": "CARIBBEAN CREAM LIMITED",
# 			"ticker": "KREMI",
# 			"industry": "MANUFACTURING",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "junior"
# 		},
# 		{
# 			"id": 36,
# 			"name": "KINGSTON WHARVES LIMITED",
# 			"ticker": "KW",
# 			"industry": "OTHER",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "main"
# 		},
# 		{
# 			"id": 111,
# 			"name": "THE LIMNERS AND BARDS LIMITED",
# 			"ticker": "LAB",
# 			"industry": "OTHER",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "junior"
# 		},
# 		{
# 			"id": 99,
# 			"name": "LASCO DISTRIBUTORS LIMITED",
# 			"ticker": "LASD",
# 			"industry": "RETAIL",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "junior"
# 		},
# 		{
# 			"id": 100,
# 			"name": "LASCO FINANCIAL SERVICES LIMITED",
# 			"ticker": "LASF",
# 			"industry": "FINANCE",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "junior"
# 		},
# 		{
# 			"id": 101,
# 			"name": "LASCO MANUFACTURING LIMITED",
# 			"ticker": "LASM",
# 			"industry": "MANUFACTURING",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "junior"
# 		},
# 		{
# 			"id": 102,
# 			"name": "LUMBER DEPOT LIMITED",
# 			"ticker": "LUMBER",
# 			"industry": "OTHER",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "junior"
# 		},
# 		{
# 			"id": 103,
# 			"name": "MAILPAC GROUP LIMITED",
# 			"ticker": "MAILPAC",
# 			"industry": "OTHER",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "junior"
# 		},
# 		{
# 			"id": 105,
# 			"name": "MEDICAL DISPOSABLES & SUPPLIES LIMITED",
# 			"ticker": "MDS",
# 			"industry": "RETAIL",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "junior"
# 		},
# 		{
# 			"id": 104,
# 			"name": "MAIN EVENT ENTERTAINMENT GROUP",
# 			"ticker": "MEEG",
# 			"industry": "OTHER",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "junior"
# 		},
# 		{
# 			"id": 38,
# 			"name": "MAYBERRY INVESTMENTS LIMITED",
# 			"ticker": "MIL",
# 			"industry": "FINANCE",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "main"
# 		},
# 		{
# 			"id": 39,
# 			"name": "MAYBERRY JAMAICAN EQUITIES LIMITED",
# 			"ticker": "MJE",
# 			"industry": "FINANCE",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "main"
# 		},
# 		{
# 			"id": 40,
# 			"name": "MPC CARIBBEAN CLEAN ENERGY LIMITED",
# 			"ticker": "MPCCEL",
# 			"industry": "OTHER",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "main"
# 		},
# 		{
# 			"id": 125,
# 			"name": "MPC CARIBBEAN CLEAN ENERGY LIMITED USD",
# 			"ticker": "MPCCELUSD",
# 			"industry": "OTHER",
# 			"type": "ORDINARY",
# 			"currency": "USD",
# 			"market": "usd"
# 		},
# 		{
# 			"id": 37,
# 			"name": "MARGARITAVILLE (TURKS) LIMITED",
# 			"ticker": "MTL",
# 			"industry": "TOURISM",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "main"
# 		},
# 		{
# 			"id": 124,
# 			"name": "MARGARITAVILLE (TURKS) LIMITED USD",
# 			"ticker": "MTLUSD",
# 			"industry": "TOURISM",
# 			"type": "ORDINARY",
# 			"currency": "USD",
# 			"market": "usd"
# 		},
# 		{
# 			"id": 41,
# 			"name": "NCB FINANCIAL GROUP LIMITED ",
# 			"ticker": "NCBFG",
# 			"industry": "FINANCE",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "main"
# 		},
# 		{
# 			"id": 42,
# 			"name": "PALACE AMUSEMENT CO. LTD.",
# 			"ticker": "PAL",
# 			"industry": "OTHER",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "main"
# 		},
# 		{
# 			"id": 126,
# 			"name": "PRODUCTIVE BUSINESS SOLUTION LTD USD ORDINARY SHARES",
# 			"ticker": "PBS",
# 			"industry": "OTHER",
# 			"type": "ORDINARY",
# 			"currency": "USD",
# 			"market": "usd"
# 		},
# 		{
# 			"id": 43,
# 			"name": "PANJAM INVESTMENT LIMITED",
# 			"ticker": "PJAM",
# 			"industry": "CONGLOMERATES",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "main"
# 		},
# 		{
# 			"id": 44,
# 			"name": "PORTLAND JSX LIMITED",
# 			"ticker": "PJX",
# 			"industry": "FINANCE",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "main"
# 		},
# 		{
# 			"id": 46,
# 			"name": "PROVEN INVESTMENTS LIMITED JMD",
# 			"ticker": "PROVEN",
# 			"industry": "FINANCE",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "main"
# 		},
# 		{
# 			"id": 127,
# 			"name": "PROVEN INVESTMENTS LIMITED USD",
# 			"ticker": "PROVENUSD",
# 			"industry": "FINANCE",
# 			"type": "ORDINARY",
# 			"currency": "USD",
# 			"market": "usd"
# 		},
# 		{
# 			"id": 106,
# 			"name": "PARAMOUNT TRADING (JAMAICA) LIMITED",
# 			"ticker": "PTL",
# 			"industry": "MANUFACTURING",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "junior"
# 		},
# 		{
# 			"id": 47,
# 			"name": "PULSE INVESTMENTS LIMITED",
# 			"ticker": "PULS",
# 			"industry": "OTHER",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "main"
# 		},
# 		{
# 			"id": 78,
# 			"name": "CONSOLIDATED BAKERIES (JAMAICA) LIMITED",
# 			"ticker": "PURITY",
# 			"industry": "MANUFACTURING",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "junior"
# 		},
# 		{
# 			"id": 48,
# 			"name": "QWI INVESTMENTS LIMITED",
# 			"ticker": "QWI",
# 			"industry": "FINANCE",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "main"
# 		},
# 		{
# 			"id": 49,
# 			"name": "RADIO JAMAICA LIMITED",
# 			"ticker": "RJR",
# 			"industry": "COMMUNICATIONS",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "main"
# 		},
# 		{
# 			"id": 93,
# 			"name": "IRONROCK INSURANCE COMPANY LIMITED",
# 			"ticker": "ROC",
# 			"industry": "INSURANCE",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "junior"
# 		},
# 		{
# 			"id": 54,
# 			"name": "SALADA FOODS JAMAICA LTD.",
# 			"ticker": "SALF",
# 			"industry": "MANUFACTURING",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "main"
# 		},
# 		{
# 			"id": 60,
# 			"name": "SYGNUS CREDIT INVESTMENTS LIMITED JMD ORDINARY SHARES",
# 			"ticker": "SCIJMD",
# 			"industry": "FINANCE",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "main"
# 		},
# 		{
# 			"id": 61,
# 			"name": "SYGNUS CREDIT INVESTMENTS LIMITED USD ORDINARY SHARES",
# 			"ticker": "SCIJMD",
# 			"industry": "FINANCE",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "main"
# 		},
# 		{
# 			"id": 129,
# 			"name": "SYGNUS CREDIT INVESTMENTS LIMITED JMD ORDINARY SHARES",
# 			"ticker": "SCIUSD",
# 			"industry": "FINANCE",
# 			"type": "ORDINARY",
# 			"currency": "USD",
# 			"market": "usd"
# 		},
# 		{
# 			"id": 130,
# 			"name": "SYGNUS CREDIT INVESTMENTS LIMITED USD ORDINARY SHARES",
# 			"ticker": "SCIUSD",
# 			"industry": "FINANCE",
# 			"type": "ORDINARY",
# 			"currency": "USD",
# 			"market": "usd"
# 		},
# 		{
# 			"id": 52,
# 			"name": "SAGICOR SELECT FUNDS LIMITED FINANCIAL",
# 			"ticker": "SELECTF",
# 			"industry": "FINANCE",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "main"
# 		},
# 		{
# 			"id": 53,
# 			"name": "SAGICOR SELECT FUNDS LIMITED MANUFACTURING & DISTRIBUTION",
# 			"ticker": "SELECTMD",
# 			"industry": "MANUFACTURING",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "main"
# 		},
# 		{
# 			"id": 56,
# 			"name": "SEPROD LIMITED",
# 			"ticker": "SEP",
# 			"industry": "MANUFACTURING",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "main"
# 		},
# 		{
# 			"id": 55,
# 			"name": "SCOTIA GROUP JAMAICA LIMITED",
# 			"ticker": "SGJ",
# 			"industry": "FINANCE",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "main"
# 		},
# 		{
# 			"id": 58,
# 			"name": "STERLING INVESTMENTS LIMITED",
# 			"ticker": "SIL",
# 			"industry": "FINANCE",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "main"
# 		},
# 		{
# 			"id": 128,
# 			"name": "STERLING INVESTMENTS LIMITED USD",
# 			"ticker": "SILUSD",
# 			"industry": "FINANCE",
# 			"type": "ORDINARY",
# 			"currency": "USD",
# 			"market": "usd"
# 		},
# 		{
# 			"id": 50,
# 			"name": "SAGICOR GROUP JAMAICA LIMITED",
# 			"ticker": "SJ",
# 			"industry": "CONGLOMERATES",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "main"
# 		},
# 		{
# 			"id": 57,
# 			"name": "STANLEY MOTTA LIMITED ORDINARY SHARES",
# 			"ticker": "SML",
# 			"industry": "OTHER",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "main"
# 		},
# 		{
# 			"id": 109,
# 			"name": "STATIONERY AND OFFICE SUPPLIES LIMITED",
# 			"ticker": "SOS",
# 			"industry": "OTHER",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "junior"
# 		},
# 		{
# 			"id": 149,
# 			"name": "SYGNUS REAL ESTATE FINANCE LIMITED",
# 			"ticker": "SRFJMD",
# 			"industry": "OTHER",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "main"
# 		},
# 		{
# 			"id": 150,
# 			"name": "SYGNUS REAL ESTATE FINANCE LIMITED",
# 			"ticker": "SRFUSD",
# 			"industry": "OTHER",
# 			"type": "ORDINARY",
# 			"currency": "USD",
# 			"market": "main"
# 		},
# 		{
# 			"id": 108,
# 			"name": "SSL VENTURE CAPITAL JAMAICA LIMITED",
# 			"ticker": "SSLVC",
# 			"industry": "OTHER",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "junior"
# 		},
# 		{
# 			"id": 59,
# 			"name": "SUPREME VENTURES LIMITED",
# 			"ticker": "SVL",
# 			"industry": "OTHER",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "main"
# 		},
# 		{
# 			"id": 62,
# 			"name": "TRANSJAMAICAN HIGHWAY LIMITED JMD",
# 			"ticker": "TJH",
# 			"industry": "OTHER",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "main"
# 		},
# 		{
# 			"id": 131,
# 			"name": "TRANSJAMAICAN HIGHWAY LIMITED USD",
# 			"ticker": "TJHUSD",
# 			"industry": "OTHER",
# 			"type": "ORDINARY",
# 			"currency": "USD",
# 			"market": "main"
# 		},
# 		{
# 			"id": 133,
# 			"name": "TROPICAL BATTERY",
# 			"ticker": "TROPICAL",
# 			"industry": "MANUFACTURING",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "junior"
# 		},
# 		{
# 			"id": 112,
# 			"name": "TTECH LIMITED",
# 			"ticker": "TTECH",
# 			"industry": "OTHER",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "junior"
# 		},
# 		{
# 			"id": 63,
# 			"name": "VICTORIA MUTUAL INVESTMENTS LTD ORDINARY SHARES",
# 			"ticker": "VMIL",
# 			"industry": "FINANCE",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "main"
# 		},
# 		{
# 			"id": 65,
# 			"name": "WIGTON WINDFARM LIMITED ORDINARY SHARES",
# 			"ticker": "WIG",
# 			"industry": "OTHER",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "main"
# 		},
# 		{
# 			"id": 66,
# 			"name": "WISYNCO GROUP LTD ORDINARY SHARES",
# 			"ticker": "WISYNCO",
# 			"industry": "MANUFACTURING",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "main"
# 		},
# 		{
# 			"id": 51,
# 			"name": "SAGICOR REAL ESTATE X FUND LTD.",
# 			"ticker": "XFUND",
# 			"industry": "OTHER",
# 			"type": "ORDINARY",
# 			"currency": "JMD",
# 			"market": "main"
# 		}
# 	]
# }