# -*- coding: utf-8 -*-
import requests, re
s=requests.get("https://obd-memorial.ru/html/search.htm?f=измайлов&n=&s=&y=&r=&p=1", allow_redirects=True)
print(s.status_code)
if(s.status_code==307):
    print(s.cookies["JSESSIONID"])
    print(s.cookies)
    print(s.cookies["3fbe47cd30daea60fc16041479413da2"])
    cookies = {'JSESSIONID': s.cookies["JSESSIONID"], "3fbe47cd30daea60fc16041479413da2":s.cookies["3fbe47cd30daea60fc16041479413da2"]}
    s=requests.get("https://obd-memorial.ru/html/search.htm?f=иванов&n=&s=&y=&r=&p=1", allow_redirects=True, cookies=cookies)
    print(s.cookies)
    match = re.search(r'countPages = \d+',s.text,)
    if match:
        m1=re.search(r'\d+',match[0])
        print(m1[0])

