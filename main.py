import requests
from bs4 import BeautifulSoup
import json
from dotenv import load_dotenv
import os
from requests.sessions import Request

load_dotenv()

session = requests.Session()

cookies = {
    "XSRF-TOKEN": "eyJpdiI6InNQakVFbTBSL2NVaGFGNWNJcjJBUFE9PSIsInZhbHVlIjoiNTh5dnYxeTI2SDlBQjRGREw1eEtreVFjM0FOaTJVTnJ3aG85bWl4SG9LdSs2MHROR21OcGo3YkRZTndGVWZyWkV5UU5wY1ZDWFoxVmFxRTJ2akVLenNrYmMzK1doZkpjaDgwR3VwSzlKOW5pSTZINkxCcGp6cUo2RUpOaWlTUG4iLCJtYWMiOiJkNDI0MTVlNzJmMzQzM2ZkM2MyZTA4MjQzZTgwYjg3NTI4Y2ZmNjJmNmExZDhmZDMwOTdiMzZjNmMwN2QzNmU3IiwidGFnIjoiIn0%3D",
    "mymoneyja_session": "eyJpdiI6ImZPYXM4K0UvdmdBTDZHZnBlOWxxU3c9PSIsInZhbHVlIjoiZ0tNbkdNVUNQMGZYdXZKUGpTQ2c5OTRReVd6bnJKcHI2VjRvME1TZlNWeGJCU0QyWU1lMVp2NEx2d1Y3T3FhcU0xR09QOEprc2VhN1BVRURvaWpBQXJpbldzZzRmd0srN2F3RkVsWm1Ed3NDYUhjWHFiakw4R1FzTkVNbWo3eTAiLCJtYWMiOiI3OTE3MTJmZTUxZDMxOTE3N2JiZTIxNjY0N2ZhM2QwODBmOGJjODNhNWNiZDJjMmViY2ZlYTQ3YjA1MGFiYTBkIiwidGFnIjoiIn0%3D",
    "crisp-client%2Fsession%2F595850e5-08f3-4ce7-82e8-129ab88f150c": "session_c4ac7265-44dc-4714-8f37-1f9dae4bfa38",
}

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:93.0) Gecko/20100101 Firefox/93.0",
    "Accept": "text/html, application/xhtml+xml",
    "Accept-Language": "en-US,en;q=0.5",
    "X-Requested-With": "XMLHttpRequest",
    "X-Inertia": "true",
    "X-Inertia-Version": "9e2f6c6666c6f388d3c296e25c362a23",
    "X-XSRF-TOKEN": "eyJpdiI6InQrOUpnZERMR3ZVTHNhWFVZd2hGT1E9PSIsInZhbHVlIjoicDJoa1pIdHRidzJnTlRtcHBaTm83SklpK1ArWGV3ZG1ERU9rdGZXSTBRMWRUQTJHdVBaVE8vL2xWeks3N054MmdhYStaR0VYWWtZODhjLzBQSUhSdnl6OGdkQjhDa2x2ZXFweENFM2MrK0hQdTBkTVBIQ0E5d1Z3WGlkLzFMaWYiLCJtYWMiOiI0ZDAyNGU5OWM2ZTc4NWVmY2E0MjQwOGQ2ZTVkNjc2NWUwMTQwMjNiNzgwMTdhZTBhZGNkZTVkYjI1NmI5ZjQ2IiwidGFnIjoiIn0=",
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

login_response = session.post(
    "https://mymoneyja.com/login", headers=headers, cookies=cookies, data=data
)


response = session.get(
    "https://mymoneyja.com/market/api", headers=headers, data=data, cookies=cookies
)

# get scaped data
stock_data = json.loads(response.content)

company = {}
# puts each company in a dictionary
for comp in stock_data:
    company[comp["ticker"]] = comp


# response2 = session.get(
#     "https://mymoneyja.com/stock/GK", headers=headers, data=data, cookies=cookies
# )
# soup = BeautifulSoup(response2.content, "html.parser")
# stock_data = json.loads(soup.text)
# company["GK"] = stock_data

for key in company:
    response2 = session.get(
        "https://mymoneyja.com/stock/{0}".format(key),
        headers=headers,
        data=data,
        cookies=cookies,
    )
    soup = BeautifulSoup(response2.content, "html.parser")
    # div_data = soup.find("div", id="app")
    stock_data = json.loads(soup.text)
    # stock_data = json.loads(div_data["data-page"])

    company[key] = stock_data

# print(soup)
print(company["GK"])
