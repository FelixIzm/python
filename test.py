# -*- coding: utf-8 -*-
import requests, re
import asyncio

async def main():
    URL = "https://obd-memorial.ru/html/search.htm?f=иванов&n=&s=&y=&r=&p=1"
    loop = asyncio.get_event_loop()
    future1 = loop.run_in_executor(None, requests.get, URL)
    s = await future1
    print(s.status_code)
    if(s.status_code==307):
        #print(s.cookies["JSESSIONID"])
        #print(s.cookies)
        #print(s.cookies["3fbe47cd30daea60fc16041479413da2"])
        cookies = {'JSESSIONID': s.cookies["JSESSIONID"], "3fbe47cd30daea60fc16041479413da2":s.cookies["3fbe47cd30daea60fc16041479413da2"]}
        def do_req():
            return requests.get(URL,cookies=cookies)
        future2 = loop.run_in_executor(None, do_req )
        response = await future2

        #s=requests.get(URL, cookies=cookies)
        #print(s.cookies)
        match = re.search(r'countPages = \d+',response.text,)
        if match:
            m1=re.search(r'\d+',match[0])
            return(m1[0])
        else:
            return 0 


loop = asyncio.get_event_loop()
print(loop.run_until_complete(main()))


