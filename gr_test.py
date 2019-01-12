import requests
fxReq = '/search.htm?f=пеплов&n=&s=&y=&r='
print(fxReq)
URL = "https://obd-memorial.ru/html"+fxReq

ss = requests.Session()
ww= ss.get(URL)
print(ww.status_code)
