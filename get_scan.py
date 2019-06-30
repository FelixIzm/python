#!/usr/bin/python3
# # -*- coding: utf-8 -*-
import requests, re
import asyncio,urllib.parse,json
from requests_html import HTMLSession
import pprint, hashlib, wget


#sys.tracebacklimit = None
cookies = {}
headers={}
secret_cookie = "3fbe47cd30daea60fc16041479413da2"
secret_cookie_value = ''
JSESSIONID_value = ''


def get_scaninfo(id):
    session = HTMLSession()
    global cookies,headers, writer, csv_columns
    info_url ='https://obd-memorial.ru/html/getimageinfo?id='+str(id)
    s = session.get(info_url)
    print(s.status_code)
    if(s.status_code==307):
        secret_cookie_value = s.cookies[secret_cookie]
        cookies = { secret_cookie:secret_cookie_value}
        #cookies['request']=urllib.parse.quote(url3)
        headers['cookie']=secret_cookie+"="+secret_cookie_value
        headers['cookie']=secret_cookie+"="+secret_cookie_value #+'; request='+urllib.parse.quote(url3)
        headers['authority'] = 'obd-memorial.ru'
        headers['User-Agent']='Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0'
        headers['Accept']='text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        headers['Accept-Language'] = 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3'
        headers['Accept-Encoding'] = 'gzip, deflate, br'
        headers['Connection'] = 'keep-alive'
        headers['Upgrade-Insecure-Requests']='1'
        r1 = requests.get(info_url,cookies=cookies,headers=headers)
        json_data = json.loads(r1.text)
        #json_data = r1.json()
        pprint.pprint(json_data[0])

        for scan in json_data:
            #print(scan['img'])
            id1_str = str(scan['id'])+'db76xdlrtxcxcghn7yusxjcdxsbtq1hnicnaspohh5tzbtgqjixzc5nmhybeh'
            id1 = hashlib.md5(id1_str.encode('utf-8')).hexdigest()
            image_url = 'https://obd-memorial.ru/html/images3?id='+str(scan['id'])+'&id1='+id1+'&path='+scan['img']
            print(image_url)
            out_file = 'e:\\temp\\obd\\'+str(scan['id'])+".jpg"
            r = requests.get(image_url, allow_redirects=True, stream=True,cookies=cookies,headers=headers)
            print(r.status_code)
            open(out_file, 'wb').write(r.content)

get_scaninfo(1153001484)
