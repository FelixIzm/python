import requests, asyncio,urllib.parse
from concurrent.futures import ThreadPoolExecutor


cookies = {}
headers={}
session = requests.session()
loop = asyncio.get_event_loop()
cook_key = '3fbe47cd30daea60fc16041479413da2'
cook_value = ''
URL = "https://obd-memorial.ru/html"
async def once():
    global loop,session,cook_key, URL
    future1 = loop.run_in_executor(None, session.get, URL)
    s = await future1
    if(s.status_code==307):
        if( cook_key in s.cookies.keys()):
            print(s.cookies)
            return  s.cookies[cook_key]
        else:
            loop.run_until_complete(once())

cook_value = loop.run_until_complete(once())
print(cook_value)
#pool = ThreadPoolExecutor(max_workers=multiprocessing.cpu_count())
pool = ThreadPoolExecutor(32)

async def fetch_async(pid):
    global loop
    global URL, session, headers,cook_value,cookies,pool
    decode_request = urllib.parse.quote('f=пеплов&n=&s=&y=&r=')
    URL ='https://obd-memorial.ru/html/search.htm?f='+urllib.parse.quote('пеплов',safe='')+'&n=&s=&y=&r=&p='+str(pid)
    #print(URL)
    cookies['3fbe47cd30daea60fc16041479413da2'] = cook_value
    cookies['request'] = urllib.parse.quote('f=пеплов&n=&s=&y=&r=')
    cookies['path']= '/html/search.htm?f='+urllib.parse.quote('пеплов')+'&n=&s=&y=&r='

    headers['User-Agent']='Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'
    #headers['cookie']='request=f='+urllib.parse.quote('пеплов')+'&n=&s=&y=&r=; 3fbe47cd30daea60fc16041479413da2='+cook_value+';JSESSIONID=847E0845FDEB166BC741FC15A10A618F'
    headers['cookie']='_ym_uid=1546973090436036836; _ym_d=1546973090; _ga=GA1.2.611230190.1546973092; 3fbe47cd30daea60fc16041479413da2=342af71acdbc4177a6f0bc3abe1a57d4; _ym_isad=2; _ym_visorc_47526808=w; _gid=GA1.2.1579188414.1549729144; request=f%3D%D0%BF%D0%B5%D0%BF%D0%BB%D0%BE%D0%B2%26n%3D%26s%3D%26y%3D%26r%3D; JSESSIONID=9E0AA96E34035F28E06FC15855DC8499;' 
    headers['referer']='https://obd-memorial.ru/html/search.htm?f='+urllib.parse.quote('пеплов')+'&n=&s=&y=&r='
    def do_req():
        return requests.get(URL,cookies=cookies,headers=headers)
    future1 = loop.run_in_executor(None, do_req )
    response = await future1
    result=response.cookies.keys()

    if('search_ids' not in result):
        if('JSESSIONID' in result):
            cookies['JSESSIONID'] = response.cookies['JSESSIONID']
            headers['Cache-Control']='max-age=0'
        else:
            return None
        def do_req1():
            return requests.get(URL,cookies=cookies,headers=headers)
        future2 = loop.run_in_executor(None, do_req1 )
        response = await future2
        if('search_ids' not in response.cookies.keys()):
            def do_req2():
                return requests.get(URL,cookies=cookies,headers=headers)
            future3 = loop.run_in_executor(None, do_req2 )
            response = await future3
            result=response.cookies.keys()
    
    return response.cookies


async def asynchronous():
    futures = [fetch_async(i) for i in range(1, 7)]
    for i, future in enumerate(asyncio.as_completed(futures)):
        result = await future
        if ('search_ids' in result):
            print('{} {} '.format(i, result['search_ids']))

loop.run_until_complete(asynchronous())
loop.close()
