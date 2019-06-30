from requests_html import HTMLSession
import json,requests

session = HTMLSession()

cookies = {}
cookies['PHPSESSID'] = 'ob6bh8easkjetr55vmcetesvv6'
cookies['LNG'] = 'ru'

data = {"indices":["gwar"],"entities":["chelovek_donesenie","chelovek_gospital","chelovek_zahoronenie","chelovek_plen","chelovek_nagrazhdenie","chelovek_predstavlenie","chelovek_nagradnaya_kartochka","commander","person","chelovek_posluzhnoi_spisok","chelovek_uchetnaya_kartochka"],"queryFields":{"ids":"","last_name":"","first_name":"","middle_name":"","birth_place":"","birth_place_gubernia":" Тверская","birth_place_uezd":"","birth_place_volost":"","location":"","birth_date":"","rank":"","data_vibitiya":"","event_name":"","event_id":"","military_unit_name":"","event_place":"","lazaret_name":"","camp_name":"","date_death":"","award_name":"","nomer_dokumenta":"","data_dokumenta":"","data_i_mesto_priziva":"","archive_short":"","nomer_fonda":"","nomer_opisi":"","nomer_dela":"","date_birth":"","data_vibitiya_end":""},"filterFields":{},"from":0,"size":"10","builderType":"Heroes"}
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}


headers['X-Requested-With'] = 'XMLHttpRequest'
headers['Content-type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'
headers['Accept-Encoding'] = 'utf-8'
headers['Connection'] = 'keep-alive'
headers['Cache-Control'] = 'no-cache'

headers['Referer'] ='https://gwar.mil.ru/heroes' #/?groups=awd:ptr:frc:cmd:prs&types=awd_nagrady:awd_kart:potery_doneseniya_o_poteryah:potery_gospitali:potery_spiski_zahoroneniy:potery_voennoplen:frc_list:cmd_commander:prs_person&page=1&birth_place_uezd=%D0%9A%D0%B0%D0%BB%D1%8F%D0%B7%D0%B8%D0%BD%D1%81%D0%BA%D0%B8%D0%B9'
headers['Host'] = 'gwar.mil.ru'
headers['Origin'] = 'https://gwar.mil.ru'

r = requests.post("https://gwar.mil.ru/gt_data/?builder=Heroes", data=json.dumps(data), headers=headers,cookies=cookies)
#print(len(json.loads(r.text)['records']))
print(r.text)