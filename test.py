# -*- coding: utf-8 -*-
import requests, re
import asyncio,urllib.parse
from requests_html import HTMLSession
import csv,sys
sys.tracebacklimit = None
cookies = {}
headers={}
secret_cookie = "3fbe47cd30daea60fc16041479413da2"
secret_cookie_value = ''
JSESSIONID_value = ''
countPages = ''
headers['User-Agent']='Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'
loop = asyncio.get_event_loop()
fio = 'юрак'
url1= 'https://obd-memorial.ru/html'
url2 = '/search.htm?'
url3= 'f='+fio+'&n=&s=&y=&r=&ps=100'
csv_columns = ['ID','Фамилия']
csv_columns.append('Имя')
csv_columns.append('Отчество')
csv_columns.append('Дата рождения/Возраст')
csv_columns.append('Место рождения')
csv_columns.append('Дата и место призыва')
csv_columns.append('Последнее место службы')
csv_columns.append('Воинское звание')
csv_columns.append('Причина выбытия')
csv_columns.append('Дата выбытия')
#csv_columns.append('')
#csv_columns.append('')
dict_data = []

csvfile = open('names.csv', 'w', newline='')
#writer = csv.writer(csvfile,delimiter=' ', quoting=csv.QUOTE_MINIMAL)
writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
writer.writeheader()

def excepthook(type, value, traceback):
    print(value)

sys.excepthook = excepthook

def main(f):
    global JSESSIONID_value, secret_cookie,secret_cookie_value, countPages, headers, cookies
    URL = 'https://obd-memorial.ru/html'
    URL_search = URL + '/search.htm?f='+f+'&n=&s=&y=&r=&ps=100'
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
if(countPages==''):
    #raise Exception('Не определилось число страниц')
    raise ValueError('Не определилось число страниц')
print('countPages = '+countPages)

ids=[]
async def get_page(page):
    global cookies,headers,ids
    if(page==0):
        URL_search =url1+url2+url3
        cookies[secret_cookie]=secret_cookie_value
        cookies['request']=urllib.parse.quote(url3)
        headers['cookie']=secret_cookie+"="+secret_cookie_value
        res1 = requests.get(URL_search,cookies=cookies,headers=headers)
        if('JSESSIONID' in res1.cookies.keys()):
            cookies[secret_cookie]=secret_cookie_value
            cookies['request']=urllib.parse.quote(url3)
            cookies['JSESSIONID'] = JSESSIONID_value
            print('URL = '+URL_search)
            res2 = requests.get(URL_search,cookies=cookies,headers=headers)
            if('search_ids' in res2.cookies.keys()):
                ids.append(res2.cookies['search_ids'])
                return res2.cookies
            else:
                while not ('search_ids' in res2.cookies.keys()):
                    res2 = requests.get(URL_search,cookies=cookies,headers=headers)
                ids.append(res2.cookies['search_ids'])
                return res2.cookies
    else:
        URL_search =url1+url2+url3+'&p='+str(page+1)
        cookies[secret_cookie]=secret_cookie_value
        cookies['request']=urllib.parse.quote(url3)
        cookies['JSESSIONID'] = JSESSIONID_value
        cookies['ids'] = ids[page-1]
        cookies['search_ids'] = ids[page-1]
        #cookies['count']='103'
        res1 = requests.get(URL_search,cookies=cookies,headers=headers)
        if(secret_cookie in res1.cookies.keys()):
            res2 = requests.get(URL_search,cookies=cookies,headers=headers)
            if('search_ids' in res2.cookies.keys()):
                ids.append(res2.cookies['search_ids'])
                return res2.cookies
            else:
                while not ('search_ids' in res2.cookies.keys()):
                    res2 = requests.get(URL_search,cookies=cookies,headers=headers)
                ids.append(res2.cookies['search_ids'])
                return res2.cookies

def get_info(id):
    session = HTMLSession()
    global cookies,headers, writer, dict_data, csv_columns
    info_url ='https://obd-memorial.ru/html/info.htm?id='+id
    res3 = session.get(info_url,cookies=cookies,headers=headers)
    list_title = res3.html.find('.card_param-title')
    list_result = res3.html.find('.card_param-result')

    row_data={}
    for x in range(len(list_result)):
        if(x==0):
            row_data['ID'] = str(id)
        else:
            if(list_title[x].text in csv_columns):
                row_data[list_title[x].text] = list_result[x-1].text
    dict_data.append(row_data)




async def fxMain():
    global countPages, writer, dict_data
    futures = [get_page(i) for i in range(0, int(countPages))]
    for i, future in enumerate(futures):
        result = await future
        if ('search_ids' in result.keys()):
            array_ids = urllib.parse.unquote( result['search_ids']).split(' ')
            print('{} {} '.format(i, len(array_ids)))
            for id in array_ids:
                get_info(id)
    for data in dict_data:
        writer.writerow(data)

loop.run_until_complete(fxMain())
loop.close()