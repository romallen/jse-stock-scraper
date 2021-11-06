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
    "XSRF-TOKEN": "eyJpdiI6Imt3YmdPU01CRUVuSmZVemhIN280R3c9PSIsInZhbHVlIjoiZlQ3c1I2YXk4SzlNdGlvZGJFYlpNY2pUNnp0RWd6NzV6QlpLT3NTWit3TmJNajZJRStEem8yWHhtVkR3a3RZTDJCdzJaeHpIWHJNWEtNVFBpSE51NmFUMUN4SDV5WWVwZm5ybUNsSVZCNzZBTndqd0ZKbmtlR3V5YVMzdWc4TzkiLCJtYWMiOiJjNDM1YzBkNjY5ZGQyODljYTg1MzAxMTY1NGJmZmY4Y2EwYzY1YWZmZjZjOGFkNDQwYzA1NjlkNThkMDg3Y2Q2IiwidGFnIjoiIn0%3D",
    "mymoneyja_session": "eyJpdiI6Ik53elFVQjZjVTJ6MEpFeXlPdTFyNUE9PSIsInZhbHVlIjoiQzFMS1FpenlsbW5Mb3BtalZNTUtsVnNqVW5xc3lVZk52TldrOTZmYTlORm8zNmp6NFIxSVF3d1Z0K1ZtS1ZjdHZ4QXlWWW1zbTFmb0FTQjFJdjRPeVRxMWhwUmdpMXYwaytKeThLSjdSdnN4RUJaK1JPejVSSVpzWERuS0M3N1IiLCJtYWMiOiI4MTljNjM5ZDhhYTMxY2Y2OGY4YWVkOWY5MjgzZTg2Yjc4MzgwMTYyYTE4MGM2MTk2OTE3ODQ0OTI5Y2NlMjljIiwidGFnIjoiIn0%3D",
    "remember_web_3dc7a913ef5fd4b890ecabe3487085573e16cf82": "eyJpdiI6IkJTem44d1M0cE1CRTVLRDY0OTYzK3c9PSIsInZhbHVlIjoiTUV4emtZdFFnbnJ4K2RIUFVkWVk2WXd1SVBRR2dYOW93elMyWkQyNkpQbFFTYjhvRWxabFBaWE0ySm5EZFQwTWdHak5tL2lMUmFreXViMlRYelp2NU5pa2VLaUlCcDdnNFo2QUJ3elNmTitGL0dKZTIzTHlueE1UeXJMMlNBbnNrVmpnbFgrdW9RM0Iza3pyc0xOekl1cXJIVFp6QTd6SXQ1YWJCU21PSkU5OEpNdFpuL3lKZFBDWll3MFZ5bmV5WEZDVDVVQ2dhTzJDeGRaOVo1OTZXdkhJTEJlL2JlK29EOHQ4VWU3aW1wND0iLCJtYWMiOiI0NTlmMmYxOGIwNjkwMWU2MjY3ZDI2ZmMyZWFkNzFkOGRkZjhjMTRkYTg1MzJjM2IyYzcxMWVkYzhlNWMyZjg2IiwidGFnIjoiIn0%3D",
}

# cookies = {
#     # "__stripe_mid": "a8bcd5ba-e3e6-4a0b-8e3e-1af707d36cb9cf9014",
#     "crisp-client%2Fsession%2F595850e5-08f3-4ce7-82e8-129ab88f150c": "session_0a4fa675-f4f7-4e01-8854-e98c8f972a1d",
#     "XSRF-TOKEN": "eyJpdiI6InJTWjNydDhpVC92djFkZVlZSFNGZHc9PSIsInZhbHVlIjoiRDVaQXptcTdkbWlWYUU1ZDVPYWJRUXNYMnBvL29Xa1hUVU02djFIWklmRFlOSFd4U1B3dk02di90K0UxOEZYcHNWU2JoYVJmWWREZStSamlqL3hDUEtpTEJhNzFBSFp4UndZN1FlbkllVEc0TWYrYVpscC8wSzJxejBHSzl5alAiLCJtYWMiOiJiYmM4N2I0YTliNTgyYTdiM2U1MTk0YTNlZTdmM2FhZThkMTZmMGIxMzYyNjBkYzhhNDgwMDA2YTZhZDRiYTIzIiwidGFnIjoiIn0%3D",
#     "mymoneyja_session": "eyJpdiI6ImZOdWo5azIwWmNZZmRwZE5uLzY5d3c9PSIsInZhbHVlIjoicnE4SUljeDhrMTd6VDBDSXhHMnpIMGQ1VUsyNCt1OHl3V29ScWZBME9jZkhqL3d5M2E5SG9nM01uaU1ZVzI0NE5SQjkyWS9QMjNtTENoYm9aWGN6eDNyYVQ3VjlqSHRSV3I2Q1FGdWV1b2VZYUlFcERzdFRHSUxxMHVoQzVoZ0YiLCJtYWMiOiIzYTdlMzI5ZGYwMzcxZTVmOGM3ZDUyZTY1MzQ5ZDE3N2M2OWNjYTU4MWNhZjZiMmYzODI0YmZlMTg1MzI1NmYyIiwidGFnIjoiIn0%3D",
#     # "remember_web_3dc7a913ef5fd4b890ecabe3487085573e16cf82": "eyJpdiI6IlpJaDhGbFVEMXg1MzNBYk5GY3NoZnc9PSIsInZhbHVlIjoiSkVsenlJeGc3U0F0OFhDWnNmc081OWJDZFR3SkNGWW9kMjNRcE04ay8zZFh2ZkUvVzBKSVpvVHltOEwyRFpwcHhRNjZNQ0dNTjN5enNPS1BhTlZiWndhcXgyaUdxN0NTTzQwekVBRkpYaDVhdGtRTjNDS0VVK3Bmdko5a0VRT3JMRGRDV1JoWnlqbWptRURPNEh4OWdHb0tOY1UyTHpWV21Va3RaUGNtMmkydExELzJMY3dPb2hPYkxhVzhLb09OcVBDVXJsM3NYUzEzNVo3dDVSL0FGdmxNcDF6QnFtZXd6VkdOemg3d0Jlcz0iLCJtYWMiOiIwYWI5MzVkZTAyZTVlOGRhYTI1YzVkOWViNzQ3YjdmYThkZDM1OWI1MzEzZGI3NmYzOGJkNmIzZGE0MjNmYjNhIiwidGFnIjoiIn0%3D",
# }

session.headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:93.0) Gecko/20100101 Firefox/93.0",
    "Accept": "text/html, application/xhtml+xml",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": "application/json",
    "X-Requested-With": "XMLHttpRequest",
    "X-Inertia": "true",
    "X-Inertia-Version": "ad2ee72ba18d474f9d1f72d2823694c4",
    "X-XSRF-TOKEN": "eyJpdiI6ImMxdmw1c1pGZVMxTExFb3A1SEZ1WUE9PSIsInZhbHVlIjoiMjVUZ3grOGZyOU5BcTI5SFp5RXU0eWcxMkUwdU1qVm1MM1o3dXJMRGYraU9KOXVIV05QcGpxZjdoNlBEanAyWWd5M1VHUnlvR1dUT2FPamd5ell5bm1kbHlOS3N3RVZPYVFLZDF1Q3oxMnZXOVIxV2RNRnhOZnNMTXRFUzBuRk4iLCJtYWMiOiI0YmJjZDg2MzQyYzBmNTk2MTczNjI4Mzc4NzllMGEwNjA3ZTA2ZDMxYjU4ZTY5YWVkYTZhMmZhYzk3NGQ4YWZjIiwidGFnIjoiIn0=",
    "Origin": "https://mymoneyja.com",
    "Connection": "keep-alive",
    "Referer": "https://mymoneyja.com/login",
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


login()
response = session.get("https://mymoneyja.com/stock/138SL", data=data)

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
        # headers=headers,
        data=data,
        # cookies=cookies,
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
