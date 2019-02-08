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
    cookies = {'3fbe47cd30daea60fc16041479413da2':cook_value, 'JSESSIONID':'9D65494D96D0615055CFAE05999998B0','request':urllib.parse.quote('f=пеплов&n=&s=&y=&r=')}
    cookies['path']= '/html/search.htm?f=%D0%BF%D0%B5%D0%BF%D0%BB%D0%BE%D0%B2&n=&s=&y=&r='

    headers['User-Agent']='Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'
    headers['cookie']='request='+urllib.parse.quote('f=пеплов&n=&s=&y=&r=')+'; 3fbe47cd30daea60fc16041479413da2='+cook_value
    headers['referer']='https://obd-memorial.ru/html/search.htm?f=%D0%BF%D0%B5%D0%BF%D0%BB%D0%BE%D0%B2&n=&s=&y=&r='

    def do_req():
        return requests.get(URL,cookies=cookies,headers=headers)
    future1 = loop.run_in_executor(pool, do_req )
    response = await future1
    result=response.cookies.keys()
    #print(result)

    while  ('search_ids' not in result):
        future1 = loop.run_in_executor(pool, do_req )
        response = await future1
        result=response.cookies.keys()
    return response.cookies


async def asynchronous():
    futures = [fetch_async(i) for i in range(0, 16)]
    for i, future in enumerate(asyncio.as_completed(futures)):
        result = await future
        if ('search_ids' in result):
            print('{} {} '.format(i, result['search_ids']))

loop.run_until_complete(asynchronous())
loop.close()
