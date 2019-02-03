import requests, asyncio,urllib.parse
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
            return  s.cookies[cook_key]
        else:
            loop.run_until_complete(once())

cook_value = loop.run_until_complete(once())
print(cook_value)

async def fetch_async(pid):
    global URL, session, headers,cook_value,cookies
    URL ='https://obd-memorial.ru/html/search.htm?f='+urllib.parse.quote('пеплов',safe='')+'&n=&s=&y=&r=&p='#+str(pid)
    cookies = {'3fbe47cd30daea60fc16041479413da2':cook_value, 'JSESSIONID':'9D65494D96D0615055CFAE05999998B0'}
    headers['cookie']='request=f'+urllib.parse.quote('=пеплов&n=&s=&y=&r=')+'; 3fbe47cd30daea60fc16041479413da2='+cook_value
    print(URL)
    def do_req():
        return session.get(URL,cookies=cookies,headers=headers)
    future1 = loop.run_in_executor(None, do_req )
    response = await future1
    #print('{} {}'.format(response.status_code, response.cookies.keys()))
    #response.close()
    result=response.cookies.keys()
    print(result)

async def asynchronous():
    futures = [fetch_async(i) for i in range(0, 13)]
    for i, future in enumerate(asyncio.as_completed(futures)):
        result = await future
        #print('{} {} '.format(i, result))

loop.run_until_complete(asynchronous())
loop.close()
