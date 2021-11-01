import requests
from bs4 import BeautifulSoup
import mechanize
import http.cookiejar


# cookies = {
#     "XSRF-TOKEN": "eyJpdiI6IndQUjk1bWd6Z2NNZnM5ZTJVWlozQ2c9PSIsInZhbHVlIjoiMmhoSWVIdmd5NDhiMlhSanlDTmU5RUhnZ1BCRlVUdDlYVDBCanpWalovbHgxVnF2TlR4aWxKNFQzOStxTGVmK0VNcWtEaGNJMllqWGV1VG81SnR2VE1hZk9Gc2YxUVBGNXdvWDZoWm5IcHVPWVM0WWlwcnJkbUROMDBoNWtpb1UiLCJtYWMiOiJlYzRiNDlmYWJkM2U4ODgxNzUxODEwYjlhMDI1YTk4MjhlZWYxZDhjMTBjZWNjM2M1Y2Y2YWVkZWE1NWRhZTYxIiwidGFnIjoiIn0%3D",
#     "mymoneyja_session": "eyJpdiI6ImFhTjZGOTU1eHI2VTQxNlZ6bDFIUUE9PSIsInZhbHVlIjoidWF4c0FRN2R1bDl5bnI0YU9xWVVQZmIxWkdEcWhSZVlzSG1nc2Q3SlpGTVRhTnc1TWthRmVrMDZmcXBlcklGY3V6a3VUeVlkbWNTQ21INERWYS90bG5EZnVtN1hOYVNNWDA0RGczK09UdmFaV01iQjY5QzZsUElpWFREaTFMWm0iLCJtYWMiOiI5OGNmMDY2YTg1YTdhNjZiZDkyYmJjNWYwYmRkZDc4MjIwNjk5ODBmMWIwNmU2Nzg2MmVjNmFiNWI2YjFmNWNmIiwidGFnIjoiIn0%3D",
# }

# headers = {
#     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:93.0) Gecko/20100101 Firefox/93.0",
#     "Accept": "text/html, application/xhtml+xml",
#     "Accept-Language": "en-US,en;q=0.5",
#     "X-Requested-With": "XMLHttpRequest",
#     "X-Inertia": "true",
#     "X-Inertia-Version": "c8c700bcca69472c4b5ff1c3a8b79f3e",
#     "X-XSRF-TOKEN": "eyJpdiI6ImdLV3A0UXdPczNYMXd0dkZXY2FaZ0E9PSIsInZhbHVlIjoiaE1yNWtRVmFrT1MzTW1GNW1YZHZDVGY5WDRzelZRRnYrZGhjQVU2MzFwVGJ6dVhLejM1clJSMStVTGd0TCtpN3dIQ1BDbG9xbnV3anR0UGxTeEVIWFdlL3VXcVp0RVNjMUxPdFdYNlN3UWJIRHhLekJMaHZXMkxxYUtXWVBzM2siLCJtYWMiOiJiNjUzNDI2YmFlN2ZkYjlhOWM1NDEyN2IxYjA2NjRmZDE3OWM5OTI3OWUzNjIzYWM0N2FlOGVlNWY2MWEzOGVmIiwidGFnIjoiIn0=",
#     "Referer": "https://mymoneyja.com/login",
#     "Connection": "keep-alive",
#     "Sec-Fetch-Dest": "empty",
#     "Sec-Fetch-Mode": "cors",
#     "Sec-Fetch-Site": "same-origin",
#     "TE": "trailers",
# }

# response = requests.get(
#     "https://mymoneyja.com/market", headers=headers, cookies=cookies
# )


cookies = {
    "wassup8ff73ecbf0c3161244e29436a8850371": "MGJfZDBjOWZmMDQ0YjhhNjY0NjQ1NzgxOGY2ZDUwNjQzNGYjIzE2MzU3Njg1MjgjIzE0NDAgeCA5MDAjIzE4MC4xMS4zNy4xMjYjI3AxNDAyMTI2LWlwbmduOTUwMXNvdWthLnNhaXRhbWEub2NuLm5lLmpwIyM%253D",
    "pmpro_visit": "1",
    "wassup_screen_res8ff73ecbf0c3161244e29436a8850371": "1440%20x%20900",
    "_ga": "GA1.2.248101527.1635765834",
    "_gid": "GA1.2.152014990.1635765834",
    "wordpress_test_cookie": "WP%20Cookie%20check",
    "wordpress_logged_in_f45d1d564cf0c5ddc806b158e3ae8487": "xkalyba%7C1636975921%7CVSJAaLHI9UwwxpMMotPdssaMKPaG0QXXDBUoeHNta0K%7Ce3ccc702a90cd2426353fcb733bf896b22d4870211f4184ece4e245f8e579172",
    "_gat_gtag_UA_221271_8": "1",
}

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:93.0) Gecko/20100101 Firefox/93.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Cache-Control": "max-age=0",
}

params = (("ticker", "jse-gk"),)

response = requests.get(
    "https://moneymax101.com/company/", headers=headers, params=params, cookies=cookies
)

# NB. Original query string below. It seems impossible to parse and
# reproduce query strings 100% accurately so the one below is given
# in case the reproduced version is not "correct".
# response = requests.get('https://moneymax101.com/company/?ticker=jse-gk', headers=headers, cookies=cookies)
soup = BeautifulSoup(response.content, "html.parser")
print(soup)
