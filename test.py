# -*- coding: utf-8 -*-
import requests, re
import asyncio,urllib.parse

cookies = {}
headers={}
secret_cookie = "3fbe47cd30daea60fc16041479413da2"
secret_cookie_value = ''
JSESSIONID_value = ''
countPages = ''
headers['User-Agent']='Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'
loop = asyncio.get_event_loop()
fio = 'пеплов'
def main(f):
    global JSESSIONID_value, secret_cookie,secret_cookie_value, countPages, headers, cookies
    URL = 'https://obd-memorial.ru/html'
    URL_search = URL + '/search.htm?f='+f+'&n=&s=&y=&r='
    s = requests.get(URL)
 
    if(s.status_code==307):
        secret_cookie_value = s.cookies[secret_cookie]
        cookies = { secret_cookie:secret_cookie_value}
        headers['cookie']=secret_cookie+"="+secret_cookie_value
        r1 = requests.get(URL_search,cookies=cookies,headers=headers)
        if('JSESSIONID' in r1.cookies.keys()):
            JSESSIONID_value =  r1.cookies["JSESSIONID"]
            cookies = {'JSESSIONID': JSESSIONID_value, secret_cookie:secret_cookie_value}
            headers['JSESSIONID'] = JSESSIONID_value

            r2 = requests.get(URL_search,cookies=cookies,headers=headers)
            match = re.search(r'countPages = \d+',r2.text,)
            if match:
                m1=re.search(r'\d+',match[0])
                countPages = (m1[0])

            print('search_ids' in r2.cookies.keys())
            #print(r2.cookies['search_ids'])


main(fio)
print('secret cookie = '+secret_cookie_value)
print('JSESSIONID = '+JSESSIONID_value)
print('countPages = '+countPages)

async def fetch_async(pid, f):
    global cookies, headers,secret_cookie,secret_cookie_value
    URL_search ='https://obd-memorial.ru/html/search.htm?f='+fio+'&n=&s=&y=&r=&p='+str(pid)
    def do_req():
        return requests.get(URL_search,cookies=cookies,headers=headers)
    #future1 = loop.run_in_executor(None, do_req )
    #response = await future1
    r1 = do_req()
    #r=response.cookies.keys()
    if('JSESSIONID' in r1.cookies.keys()):
        JSESSIONID_value =  r1.cookies["JSESSIONID"]
        cookies = {'JSESSIONID': JSESSIONID_value, secret_cookie:secret_cookie_value}
        cookies['request'] = urllib.parse.quote('f=пеплов&n=&s=&y=&r=')
        headers['JSESSIONID'] = JSESSIONID_value
        headers['referer']='https://obd-memorial.ru/html/search.htm?f='+urllib.parse.quote('пеплов')+'&n=&s=&y=&r='

        r2 = requests.get(URL_search,cookies=cookies,headers=headers)
        #print(r2.cookies['search_ids'])
    return r2.cookies.keys()


#loop = asyncio.get_event_loop()
#print(loop.run_until_complete(main()))

async def asynchronous():
    global countPages,fio
    countPages_int = int(countPages)
    #countPages_int=countPages_int+1
    futures = [fetch_async(i, fio) for i in range(1, countPages_int)]
    for i, future in enumerate(asyncio.as_completed(futures)):
        result = await future
        if ('search_ids' in result):
            print('{} {} '.format(i, result))

loop.run_until_complete(asynchronous())
loop.close()

