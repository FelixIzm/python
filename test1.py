# -*- coding: utf-8 -*-
import requests, re
import asyncio, random

loop = asyncio.get_event_loop()
path = '/html/search.htm?f=пеплов&n=&s=&y=&r='
URL = "https://obd-memorial.ru"+path
cookies = {}
countPages = ""
async def main(URL):
    global path
    future1 = loop.run_in_executor(None, requests.get, URL)
    s = await future1
    if(s.status_code==307):
        global cookies
        cookies = {'JSESSIONID': s.cookies["JSESSIONID"], "3fbe47cd30daea60fc16041479413da2":s.cookies["3fbe47cd30daea60fc16041479413da2"]}
        headers = dict()
        headers['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        #headers['cookie'] = cookies
        headers['path'] = path
        headers['method']='GET'
        headers['authority']='obd-memorial.ru'
        def do_req():
            return requests.get(URL,cookies=cookies)
        future2 = loop.run_in_executor(None, do_req )
        response = await future2
        print('status_code_1={}'.format(response.status_code))
        match = re.search(r'countPages = \d+',response.text,)
        if match:
            m1=re.search(r'\d+',match[0])
            return(m1[0])
        else:
            return -1 
    else:
        print('status_code_2={}'.format(s.status_code))
        match = re.search(r'countPages = \d+',s.text,)
        if match:
            m1=re.search(r'\d+',match[0])
            return(m1[0])
        else:
            return -2

countPages = loop.run_until_complete(main(URL))
print(countPages)

async def fetch_async(pid):
    global URL
    global cookies
    URL = URL+"&p="+str(pid)
    def do_req():
        return requests.get(URL,cookies=cookies)
    future1 = loop.run_in_executor(None, do_req )
    response = await future1
    cook = response.cookies.keys()
    print('{} {} '.format(response.status_code,cookies))
    #response.close()
    return response.status_code

async def asynchronous():
    global countPages
    futures = [fetch_async(i) for i in range(0, int(countPages)+1)]
    for i, future in enumerate(asyncio.as_completed(futures)):
        result = await future
        #print('{} {} '.format(i, result))


loop.run_until_complete(asynchronous())
loop.close()
