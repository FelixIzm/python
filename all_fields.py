#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests, re
import asyncio,urllib.parse
from requests_html import HTMLSession
import csv,sys

import sqlite3
conn = sqlite3.connect("./db/all_fields.db") # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()
 
# Создание таблицы
cursor.execute("DROP TABLE if exists search_ids")
cursor.execute("DROP TABLE if exists cookies")
cursor.execute("DROP TABLE if exists headers")
cursor.execute("CREATE TABLE if not exists search_ids (id integer, flag integer, csv text)")
cursor.execute("CREATE TABLE cookies (key text, value text )")
cursor.execute("CREATE TABLE headers (key text, value text )")


sys.tracebacklimit = None
cookies = {}
headers={}
secret_cookie = "3fbe47cd30daea60fc16041479413da2"
secret_cookie_value = ''
JSESSIONID_value = ''
countPages = ''
headers['User-Agent']='Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'
loop = asyncio.get_event_loop()
########################################################
text= 'lp=P~227 сд'
########################################################
url1= 'https://obd-memorial.ru/html'
url2 = '/search.htm?'
ps = '100'
#url3= 'pb=T~'+text+'&entity=000000011111110&entities=24,28,27,23,34,22,20,21&ps='+ps
#url3= text+'&entity=000000011111110&entities=24,28,27,23,34,22,20,21&ps='+ps
url3='n=P~иван&entity=000000000100000&entities=27&ps=100'
# место выбытия
url3='pb=T~горьковская обл&entity=000000011111110&entities=24,28,27,23,34,22,20,21&ps=100'

def excepthook(type, value, traceback):
    print(value)

sys.excepthook = excepthook

def main(text):
    global JSESSIONID_value, secret_cookie,secret_cookie_value, countPages, headers, cookies, url2,url3
    URL = 'https://obd-memorial.ru/html'
    URL_search = URL + '/search.htm?'+url3
    s = requests.get('https://obd-memorial.ru/html/advanced-search.htm')
    print(s.status_code)
    if(s.status_code==307):
        secret_cookie_value = s.cookies[secret_cookie]
        cookies = { secret_cookie:secret_cookie_value}
        cookies['request']=urllib.parse.quote(url3)
        headers['cookie']=secret_cookie+"="+secret_cookie_value
        headers['path'] = '/html/search.htm?'+urllib.parse.quote(url3)
        headers['referer']='https://obd-memorial.ru/html/advanced-search.htm'
        headers['cookie']=secret_cookie+"="+secret_cookie_value+'; request='+urllib.parse.quote(url3)
        headers['referer']='https://obd-memorial.ru/html/advanced-search.htm'
        headers['authority'] = 'obd-memorial.ru'
        headers['User-Agent']='Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0'
        headers['Accept']='text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        headers['Accept-Language'] = 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3'
        headers['Accept-Encoding'] = 'gzip, deflate, br'
        headers['Connection'] = 'keep-alive'
        headers['Upgrade-Insecure-Requests']='1'
        headers['path'] = '/html/search.htm?'+urllib.parse.quote(url3)
        r1 = requests.get(URL_search,cookies=cookies,headers=headers)
        if('JSESSIONID' in r1.cookies.keys()):
            #print(r1.cookies)
            JSESSIONID_value =  r1.cookies["JSESSIONID"]
            cookies = {'JSESSIONID': JSESSIONID_value, secret_cookie:secret_cookie_value}
            cookies['request']=urllib.parse.quote(url3)
            cookies['showExtendedParams']='false'
            headers['JSESSIONID'] = JSESSIONID_value
            headers['referer']='https://obd-memorial.ru/html/advanced-search.htm'
            headers['authority'] = 'obd-memorial.ru'
            headers['User-Agent']='Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0'
            headers['Accept']='text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
            headers['Accept-Language'] = 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3'
            headers['Accept-Encoding'] = 'gzip, deflate, br'
            headers['Connection'] = 'keep-alive'
            headers['cookie']=secret_cookie+"="+secret_cookie_value+'; request='+urllib.parse.quote(url3)+'; JSESSIONID='+JSESSIONID_value
            headers['Upgrade-Insecure-Requests']='1'
            headers['path'] = '/html/search.htm?'+urllib.parse.quote(url3)

            r2 = requests.get(URL_search,cookies=cookies,headers=headers)
            match = re.search(r'countPages = \d+',r2.text)
            if match:
                m1=re.search(r'\d+',match[0])
                countPages = (m1[0])
            if(countPages==''):
                #raise Exception('Не определилось число страниц')
                raise ValueError('Не определилось число страниц!')

            for key, value in cookies.items():
                sql= 'insert into cookies (key, value) VALUES("'+key+'","'+value+'")'
                cursor.execute(sql)
            for key, value in headers.items():
                sql= 'insert into headers (key, value) VALUES("'+key+'","'+value+'")'
                cursor.execute(sql)
            conn.commit


main(text)
print('secret cookie = '+secret_cookie_value)
print('JSESSIONID = '+JSESSIONID_value)
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


async def fxMain():
    global countPages, writer
    futures = [get_page(i) for i in range(0, int(countPages))]
    for i, future in enumerate(futures):
        result = await future
        if ('search_ids' in result.keys()):
            array_ids = urllib.parse.unquote( result['search_ids']).split(' ')
            print('{} {} {} '.format(i, countPages, len(array_ids)))
            for id in array_ids:
                #get_info(id)
                cursor.execute('insert into search_ids(id,flag) values ('+id+',0)')
            conn.commit()


loop.run_until_complete(fxMain())
loop.close()