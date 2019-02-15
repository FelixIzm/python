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
fio = 'измайлов'
url1= 'https://obd-memorial.ru/html'
url2 = '/search.htm?'
url3= 'f='+fio+'&n=&s=&y=&r='
def main(f):
    global JSESSIONID_value, secret_cookie,secret_cookie_value, countPages, headers, cookies
    URL = 'https://obd-memorial.ru/html'
    URL_search = URL + '/search.htm?f='+f+'&n=&s=&y=&r='
    s = requests.get(URL)
    print(s.status_code)
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
ids=[]
async def get_page(page):
    global cookies,headers,ids
    #print('page = '+str(page))
    if(page==1):
        URL_search =url1+url2+url3
        cookies[secret_cookie]=secret_cookie_value
        cookies['request']=urllib.parse.quote(url3)
        headers['cookie']=secret_cookie+"="+secret_cookie_value
        res1 = requests.get(URL_search,cookies=cookies,headers=headers)
        #print('JSESSIONID = '+str('JSESSIONID' in res1.cookies.keys()))
        if('JSESSIONID' in res1.cookies.keys()):
            cookies[secret_cookie]=secret_cookie_value
            cookies['request']=urllib.parse.quote(url3)
            cookies['JSESSIONID'] = JSESSIONID_value
            res2 = requests.get(URL_search,cookies=cookies,headers=headers)
            if('search_ids' in res2.cookies.keys()):
                ids.append(res2.cookies['search_ids'])
                #print('prev_search_ids = '+prev_search_ids)
                #print(res2.cookies.keys())
                return res2.cookies
            else:
                while not ('search_ids' in res2.cookies.keys()):
                    res2 = requests.get(URL_search,cookies=cookies,headers=headers)
                ids.append(res2.cookies['search_ids'])
                return res2.cookies
    else:
        URL_search =URL_search =url1+url2+url3+'&p='+str(page)
        cookies[secret_cookie]=secret_cookie_value
        cookies['request']=urllib.parse.quote(url3)
        cookies['JSESSIONID'] = JSESSIONID_value
        cookies['ids'] = ids[page-2]
        cookies['search_ids'] = ids[page-2]
        #print(cookies)
        res1 = requests.get(URL_search,cookies=cookies,headers=headers)
        if(secret_cookie in res1.cookies.keys()):
            res2 = requests.get(URL_search,cookies=cookies,headers=headers)
            if('search_ids' in res2.cookies.keys()):
                ids.append(res2.cookies['search_ids'])
                #print(res2.cookies.keys())
                return res2.cookies
            else:
                while not ('search_ids' in res2.cookies.keys()):
                    res2 = requests.get(URL_search,cookies=cookies,headers=headers)
                ids.append(res2.cookies['search_ids'])
                return res2.cookies



async def fxMain():
    global countPages
    futures = [get_page(i) for i in range(1, int(countPages))]
    for i, future in enumerate(futures):
        result = await future
        if ('search_ids' in result.keys()):
            print('{} {} '.format(i, len(urllib.parse.unquote( result['search_ids']).split(' '))))

#fxMain()
loop.run_until_complete(fxMain())
loop.close()