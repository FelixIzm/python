# -*- coding: utf-8 -*-
import requests, re
import asyncio,urllib.parse
from requests_html import HTMLSession
import csv,sys,json
import sqlite3

########################################################
fio = 'Кибенко'
########################################################

conn = sqlite3.connect("./db/"+fio+".db") # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()
 
cursor.execute("SELECT * FROM cookies")
cookies = {}
for i in cursor.fetchall():
    cookies[i[0]] = i[1]
print(cookies)

cursor.execute("SELECT * FROM headers")
headers = {}
for i in cursor.fetchall():
    headers[i[0]] = i[1]
print(headers)

csvfile = open('./csv/'+fio+'.csv', 'w', newline='')
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
writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
writer.writeheader()

def get_info(id):
    session = HTMLSession()
    global cookies,headers, writer, csv_columns
    info_url ='https://obd-memorial.ru/html/info.htm?id='+str(id)
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
    #dict_data.append(row_data)
    #print(row_data)

    sql = 'update search_ids set flag = 1, csv="'+str(row_data).replace('"',"")+'" where id='+str(id)
    cursor.execute(sql)
    conn.commit()

cursor.execute("SELECT count(1) FROM search_ids where flag=0")
count_row = cursor.fetchone()[0]
#print(count_row)
count=1
cursor.execute("SELECT * FROM search_ids WHERE flag=0")
for i in cursor.fetchall():
    get_info(i[0])
    print ('{} из {}'.format(count,count_row))
    count+=1

count=1
cursor.execute("SELECT count(1) FROM search_ids where flag=1")
count_row = cursor.fetchone()[0]
cursor.execute("SELECT * FROM search_ids WHERE flag=1")
for i in cursor.fetchall():
    writer.writerow(json.loads(i[2].replace("'",'"')))
    print ('{} из {}'.format(count,count_row))
    count+=1
