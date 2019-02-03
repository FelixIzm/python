# -*- coding: utf-8 -*-
import requests, re
import asyncio, urllib

secret_cookie=sessionid=''
loop = asyncio.get_event_loop()
fxReq = '/search.htm?f=&n=&s=&y=&r='
print(fxReq)
URL = "https://obd-memorial.ru/html"+fxReq
cookies = {}
headers={}
headers['Host']='obd-memorial.ru'
headers['User-Agent']='Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'
headers['Accept']='text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
headers['Accept-Language']='ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3'
headers['Accept-Encoding']='gzip, deflate, br'
headers['Connection']='keep-alive'
#headers['Upgrade-Insecure-Requests']='1'
headers['Pragma']='no-cache'
headers['Cache-Control']='no-cache'

session = requests.session()

headers_req = headers.copy()
countPages = ""
async def main(URL):
    global headers,session
    future1 = loop.run_in_executor(None, session.get, URL)
    s = await future1
    if(s.status_code==307):
        global cookies
        global secret_cookie,jsessionid
        secret_cookie = s.cookies['3fbe47cd30daea60fc16041479413da2']
        jsessionid = s.cookies['JSESSIONID']
        print(jsessionid)
        cookies = {'3fbe47cd30daea60fc16041479413da2':secret_cookie,'JSESSIONID':jsessionid}
        def do_req():
            return session.get(URL,cookies=cookies, headers = headers)
        future2 = loop.run_in_executor(None, do_req )
        response = await future2
        #print(response.cookies)
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
    global secret_cookie,jsessionid,session
    URL = URL+"&p="+str(pid)
    #headers_req['Cookie']='request=f%3D%D0%BF%D0%B5%D0%BF%D0%BB%D0%BE%D0%B2%26n%3D%26s%3D%26y%3D%26r%3D; 3fbe47cd30daea60fc16041479413da2='+secret_cookie+'; JSESSIONID='+jsessionid
    headers_req['cookie']='request=f%3D%D0%BF%D0%B5%D0%BF%D0%BB%D0%BE%D0%B2%26n%3D%26s%3D%26y%3D%26r%3D; 3fbe47cd30daea60fc16041479413da2='+secret_cookie+'; JSESSIONID='+jsessionid
    def do_req():
        return session.get(URL,cookies=cookies,headers=headers_req)
    future1 = loop.run_in_executor(None, do_req )
    response = await future1
    #print('{} {}'.format(response.status_code, response.cookies.keys()))
    #response.close()
    result=response.cookies.keys()
    #if not ('search_ids' in result):
    #    result = await future1

    return result

async def asynchronous():
    global countPages
    futures = [fetch_async(i) for i in range(0, int(countPages)+1)]
    for i, future in enumerate(asyncio.as_completed(futures)):
        #await asyncio.sleep(1)
        result = await future
        print('{} {} '.format(i, result))


loop.run_until_complete(asynchronous())
loop.close()

