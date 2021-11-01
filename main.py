import requests
from bs4 import BeautifulSoup
import mechanize
import http.cookiejar
import json

cookies = {
    "XSRF-TOKEN": "eyJpdiI6IndQUjk1bWd6Z2NNZnM5ZTJVWlozQ2c9PSIsInZhbHVlIjoiMmhoSWVIdmd5NDhiMlhSanlDTmU5RUhnZ1BCRlVUdDlYVDBCanpWalovbHgxVnF2TlR4aWxKNFQzOStxTGVmK0VNcWtEaGNJMllqWGV1VG81SnR2VE1hZk9Gc2YxUVBGNXdvWDZoWm5IcHVPWVM0WWlwcnJkbUROMDBoNWtpb1UiLCJtYWMiOiJlYzRiNDlmYWJkM2U4ODgxNzUxODEwYjlhMDI1YTk4MjhlZWYxZDhjMTBjZWNjM2M1Y2Y2YWVkZWE1NWRhZTYxIiwidGFnIjoiIn0%3D",
    "mymoneyja_session": "eyJpdiI6ImFhTjZGOTU1eHI2VTQxNlZ6bDFIUUE9PSIsInZhbHVlIjoidWF4c0FRN2R1bDl5bnI0YU9xWVVQZmIxWkdEcWhSZVlzSG1nc2Q3SlpGTVRhTnc1TWthRmVrMDZmcXBlcklGY3V6a3VUeVlkbWNTQ21INERWYS90bG5EZnVtN1hOYVNNWDA0RGczK09UdmFaV01iQjY5QzZsUElpWFREaTFMWm0iLCJtYWMiOiI5OGNmMDY2YTg1YTdhNjZiZDkyYmJjNWYwYmRkZDc4MjIwNjk5ODBmMWIwNmU2Nzg2MmVjNmFiNWI2YjFmNWNmIiwidGFnIjoiIn0%3D",
    "crisp-client%2Fsession%2F595850e5-08f3-4ce7-82e8-129ab88f150c": "session_41886dbd-864a-4f3b-bd76-a70ea4aa69e2",
}

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:93.0) Gecko/20100101 Firefox/93.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "TE": "trailers",
}

# response = requests.get(
#     "https://mymoneyja.com/stock/GK", headers=headers, cookies=cookies
# )
response = requests.get(
    "https://mymoneyja.com/market/api", headers=headers, cookies=cookies
)

# get scaped data
soup = BeautifulSoup(response.content, "html.parser")
stock_data = json.loads(soup.text)

company = {}
# puts each company in a dictionary
for comp in stock_data:
    company[comp["ticker"]] = comp

for key in company:
    response = requests.get(
        "https://mymoneyja.com/stock/{key}", headers=headers, cookies=cookies
    )
    key_soup = BeautifulSoup(response.content, "html.parser")

    # key_stock_data = json.loads(key_soup.text)
    # company[key]["data"] = key_soup["props"]
    # company[key]["data"]["volume"] = key_stock_data["props"]["company"]["data"]["volume"]

# companies = stock_data["props"]["companies"]
print(company["1834"])
