# # -*- coding: utf-8 -*-
from requests_html import HTMLSession
import json,requests, pprint, urllib.parse

session = HTMLSession()

cookies = {}
cookies['PHPSESSID'] = 'ob6bh8easkjetr55vmcetesvv6'
cookies['LNG'] = 'ru'

#Губерния
data = u'{"indices":["gwar"],"entities":["chelovek_donesenie","chelovek_gospital","chelovek_zahoronenie","chelovek_plen","chelovek_nagrazhdenie","chelovek_predstavlenie","chelovek_nagradnaya_kartochka","commander","person","chelovek_posluzhnoi_spisok","chelovek_uchetnaya_kartochka"],"queryFields":{"ids":"","last_name":"","first_name":"","middle_name":"","birth_place":"","birth_place_gubernia":"тверская","birth_place_uezd":"","birth_place_volost":"","location":"","birth_date":"","rank":"","data_vibitiya":"","event_name":"","event_id":"","military_unit_name":"","event_place":"","lazaret_name":"","camp_name":"","date_death":"","award_name":"","nomer_dokumenta":"","data_dokumenta":"","data_i_mesto_priziva":"","archive_short":"","nomer_fonda":"","nomer_opisi":"","nomer_dela":"","date_birth":"","data_vibitiya_end":""},"filterFields":{},"from":0,"size":"10","builderType":"Heroes"}'

# ГОД РОЖДЕНИЯ 1914
#data = {"indices":["gwar"],
#   "entities":["chelovek_donesenie","chelovek_gospital","chelovek_zahoronenie","chelovek_plen","chelovek_nagrazhdenie","chelovek_predstavlenie",
#               "chelovek_nagradnaya_kartochka","commander","person","chelovek_posluzhnoi_spisok","chelovek_uchetnaya_kartochka"],
#   "queryFields":{"ids":"","last_name":"","first_name":"","middle_name":"","birth_place":"","birth_place_gubernia":"","birth_place_uezd":"",
#                   "birth_place_volost":"","location":"","birth_date":"1914","rank":"","data_vibitiya":"","event_name":"","event_id":"","military_unit_name":"",
#                   "event_place":"","lazaret_name":"","camp_name":"","date_death":"","award_name":"","nomer_dokumenta":"","data_dokumenta":"",
#                   "data_i_mesto_priziva":"","archive_short":"","nomer_fonda":"","nomer_opisi":"","nomer_dela":"","date_birth":"","data_vibitiya_end":""},
#   "filterFields":{},"from":0,"size":"10","builderType":"Heroes"}

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
headers['X-Requested-With'] = 'XMLHttpRequest'
#headers['Content-type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
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


r = requests.post("https://gwar.mil.ru/gt_data/?builder=Heroes", data=data.encode('utf-8'), headers=headers,cookies=cookies, verify=False)
pprint.pprint(json.loads(r.text)['hits']['total'])
#print(urllib.parse.quote('Тверская'))
#pprint.pprint((json.loads(r.content)['hits']['hits'][0]))