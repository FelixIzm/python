# # -*- coding: utf-8 -*-
from requests_html import HTMLSession
import json,requests, pprint, urllib.parse, asyncio, sys, csv
import sqlite3
import argparse


from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

session = HTMLSession()
cookies = {}
cookies['PHPSESSID'] = 'ob6bh8easkjetr55vmcetesvv6'
cookies['LNG'] = 'ru'
loop = asyncio.get_event_loop()

def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument ('name', nargs='?')
    return parser


#conn = sqlite3.connect('./db/gwar.db') 
conn = sqlite3.connect('e:/temp/vpp/db/gwar.db') 
cursor = conn.cursor()

if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args()
    # если что-то передали в аргументах, удаляем таблицы и все заново
    if namespace.name:
        cursor.execute("DROP TABLE if exists data")
        cursor.execute("DROP TABLE if exists pages")
        #print ("Привет, {}!".format (namespace.name) )

cursor.execute("CREATE TABLE if not exists pages (num integer)")
cursor.execute("CREATE TABLE if not exists data (id integer, csv text)")

cursor.execute("SELECT num FROM pages")
pages = cursor.fetchone()
if pages is None:
    cursor.execute('insert into pages(num) values (0)')
    conn.commit()
    insertedPages=int(0)
else:
    insertedPages = pages[0]+1

count_pages = 100

data = '''{{"indices":["gwar"],
        "entities":["chelovek_donesenie","chelovek_gospital","chelovek_zahoronenie","chelovek_plen","chelovek_nagrazhdenie","chelovek_predstavlenie",
                    "chelovek_nagradnaya_kartochka","commander","person","chelovek_posluzhnoi_spisok","chelovek_uchetnaya_kartochka"],
        "queryFields":{{"ids":"","last_name":"","first_name":"","middle_name":"","birth_place":"",
                    "birth_place_gubernia":"тверская","birth_place_uezd":"","birth_place_volost":"","location":"","birth_date":"","rank":"",
                    "data_vibitiya":"","event_name":"","event_id":"","military_unit_name":"","event_place":"","lazaret_name":"","camp_name":"",
                    "date_death":"","award_name":"","nomer_dokumenta":"","data_dokumenta":"","data_i_mesto_priziva":"","archive_short":"",
                    "nomer_fonda":"","nomer_opisi":"","nomer_dela":"","date_birth":"","data_vibitiya_end":""}},
        "filterFields":{{}},"from":{0},"size":{1},"builderType":"Heroes"}}'''




headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
headers['X-Requested-With'] = 'XMLHttpRequest'
headers['Content-type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'
headers['Accept-Encoding'] = 'utf-8'
headers['Connection'] = 'keep-alive'
headers['Cache-Control'] = 'no-cache'
headers['accept-language'] ='ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
headers['Referer'] ='https://gwar.mil.ru/heroes'
headers['Host'] = 'gwar.mil.ru'
headers['Origin'] = 'https://gwar.mil.ru'
headers['path'] = '/gt_data/?builder=Heroes'
headers['method'] = 'POST'
headers['authority'] ='gwar.mil.ru'


r = requests.post("https://gwar.mil.ru/gt_data/?builder=Heroes", data=(data.format(0,count_pages)).encode('utf-8'), headers=headers,cookies=cookies, verify=False)
#box = json.loads(r.text)['hits']['hits']
total = int((json.loads(r.text)['hits']['total']))
print(total)
total_a = range(0,int(total),count_pages)

async def get_page(page):
        global headers, cookies
        r = requests.post("https://gwar.mil.ru/gt_data/?builder=Heroes", data=(data.format(page,count_pages)).encode('utf-8'), headers=headers,cookies=cookies, verify=False)
        return r
        #box = json.loads(r.text)['hits']['hits']
        #print('{}'.format(box[0]['_source']['last_name']))

def dict_clean(dict,name_item):
        item = dict['_source'][name_item]
        if item is None:
                 item=''
        return item


async def fxMain():
        global total_a, insertedPages
        #total_a = range(0,50,4)
        futures = [get_page(insertedPages) for insertedPages in list(total_a)]
        print('insertedPages = {}'.format(insertedPages))
        print('futures.count = {}'.format(len(futures)))
        count=0
        for i, future in enumerate(futures):
                result = await future
                #print(result)
                boxes = json.loads(result.text)['hits']['hits']
                print(insertedPages)
                for box in boxes:
                        count+=1
                        data_priziva = dict_clean(box,'data_priziva')
                        last_name = dict_clean(box,'last_name')
                        first_name = dict_clean(box,'first_name')
                        middle_name = dict_clean(box,'middle_name')
                        archive_short = dict_clean(box,'archive_short') # краткое наименование архива
                        birth_date = dict_clean(box,'birth_date') # дата рождения
                        birth_place_gubernia = dict_clean(box,'birth_place_gubernia') # губерния
                        birth_place_uezd = dict_clean(box,'birth_place_uezd') #уезд
                        birth_place_volost = dict_clean(box,'birth_place_volost') # волость
                        deal = dict_clean(box,'deal') # Дело
                        vibitie_prichina = dict_clean(box,'vibitie_prichina') # Причина выбытия
                        event_date_to = dict_clean(box,'event_date_to') # Дата события
                        event_place = dict_clean(box,'event_place') # Место события
                        doc_type = dict_clean(box,'doc_type') # Тип документа
                        id = dict_clean(box,'id') # id 
                        rank = dict_clean(box,'rank') # Должность/Звание
                        military_unit_name = dict_clean(box,'military_unit_name') # Воинская часть 

                        row=[]
                        row.append(last_name)           # Фамилия
                        row.append(first_name)          # Имя
                        row.append(middle_name)         # Отчество
                        row.append(birth_date)          # Дата рождения
                        row.append(rank)                # Должность/Звание
                        row.append(military_unit_name)  # Воинская часть
                        row.append(birth_place_gubernia)# 
                        row.append(birth_place_uezd)    # 
                        row.append(birth_place_volost)  # 
                        row.append(vibitie_prichina)    # Причина выбытия
                        row.append(event_date_to)       # Дата события
                        row.append(event_place)         # Место события
                        row.append(doc_type)            # Тип документа
                        row.append(archive_short)       # Архив
                        row.append(deal)                # Дело
                        row.append('https://gwar.mil.ru/heroes/chelovek_donesenie'+str(id))
                        cursor.execute('insert into data(id,csv) values (0,"'+str(row).replace('"',"")+'")')
                        conn.commit()

                        #writer.writerow(row)
                        #print('{} {} {} {}'.format(count,last_name, first_name, middle_name))
                        #print(y)
                cursor.execute('update pages set num='+str(insertedPages))
                conn.commit()
                insertedPages+=1
 
loop.run_until_complete(fxMain())
loop.close()

'''
https://gwar.mil.ru/heroes/chelovek_donesenie14349740/

archive_short: "РГВИА"
birth_date: null
birth_place: null
birth_place_gubernia: "Тверская губ."
birth_place_id: 306787
birth_place_location: null
birth_place_np_type: "с."
birth_place_uezd: "Калязинский уезд"
birth_place_volost: "Талдомская вол."
box_id: null
data_priziva: null
deal: "Списки потерь солдат 185 пехотного Башкадыкларского полка"
deal_id: 10000619
deal_num: "352"
doc_type: "Именные списки потерь"
document_author: "185-й пехотный Башкадыкларский полк"
document_date: "1915-09-17"
document_name: "Именной список потерь нижних чинов 185 пехотного Башкадыкларского полка за июль месяц 1915 г."
document_num: 241396
documents_pages: {documents_id: [10022255], pages_id: [10208299]}
event_date_from: "1915-07-19"
event_date_to: "1915-07-19"
event_place: "Банковецкие позиции"
first_name: "Андрей"
fund: "Особое делопроизводство по сбору и регистрации сведений о выбывших за смертью или за ранами, а также пропавших без вести воинских чинах, действующих против неприятельских армий (1914 - 1918)"
fund_id: 1
fund_num: "16196"
id: 14349740
inventory: "Именные списки потерь солдат и офицеров 1 мировой войны 1914-1918 гг. (по полкам и бригадам)"
inventory_id: 1
inventory_num: "1"
last_name: "Чистов"
lazaret_id: null
middle_name: "Емельянович"
military_unit_id: 212
military_unit_name: "185-й пехотный Башкадыкларский полк"
operations: [{event_id: 62, event_name: "Польский мешок (потеря Польши)"}]
person_type: "Списки потерь"
rank: "рядовой"
shkaf: null
shkaf_id: null
shkaf_name: null
updated: "2018-10-15T00:00:00Z"
vibitie_date_from: null
vibitie_date_to: null
vibitie_mesto: null
vibitie_prichina: "пропал без вести"
zahoronenie_gubernia: null
zahoronenie_location: null
zahoronenie_mesto: null
zahoronenie_np_type: null
zahoronenie_uezd: null
zahoronenie_volost: null
__type: "chelovek_donesenie"
'''