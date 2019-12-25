import requests, re, hashlib, base64
cookies = {}
headers={}

{"bda88568a54f922fcdfc6dbf940e5d00":{"domain":"pamyat-naroda.ru","expires":"2019-12-25T15:28:57.000Z","path":"/","value":"NnBjT0RwVWdLYVlWdzhENm14aWtfd1hYWFhYWDE1NzcyODQxMzdZWVlZWVlDSWk1ZGdudXJFVEJZSEJKanRRMHF3WFhYWFhYMTU3NzI4NzczN1lZWVlZWQ"}}
headers['Host'] = 'pamyat-naroda.ru'
headers['User-Agent'] = 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0'
headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
headers['Accept-Language'] = 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3'
headers['Accept-Encoding'] = 'gzip, deflate, br'
headers['Connection'] = 'keep-alive'
headers['Cookie'] = 'BITRIX_PN_DATALINE_LNG=ru;'
headers['Upgrade-Insecure-Requests'] = '1'

cookies['BITRIX_PN_DATALINE_LNG'] = 'ru'
s = requests.Session()
url = 'https://pamyat-naroda.ru/'
res = requests.get(url, allow_redirects=False)
print(res.status_code)
print(res.cookies)
PNSESSIONID = res.cookies['PNSESSIONID']
cookie_00 = res.cookies['bda88568a54f922fcdfc6dbf940e5d00']
cookie_0b = res.cookies['56105c9ab348522591eea18fbe4d080b']
exit(1)


s ='03001222bc9570cfd8bccbf270a28ec2'
bs = 'ajRNa3dXeXVBN3doOTRZRENfZHl3d1hYWFhYWDE1NzcxODgyMTFZWVlZWVkzY2puRUl4b3JhNHViWkNhQ1kzazZnWFhYWFhYMTU3NzE5MTgxMVlZWVlZWQ'
#bs = 'Mm9EcHQ1NE80ZTh0eFNseXpQZVU4UVhYWFhYWDE1NzcxODczMDdZWVlZWVlCanliekNQTndVUkRhd19lb1NLZ093WFhYWFhYMTU3NzE5MDkwN1lZWVlZWQ'
secret_cookie = hashlib.md5(s.encode()).hexdigest()
print(secret_cookie)
url= 'https://pamyat-naroda.ru/'
s = requests.post(url)
cookie_00=s.cookies[secret_cookie]
bs += "=" * ((4 - len(cookie_00) % 4) % 4)
#print(bs)
bs = base64.b64decode(bs).decode()
a_bs = bs.split('XXXXXX')
#print(a_bs)
b_bs = a_bs[1].split('YYYYYY')
data = {"query":{"bool":{"should":[{"bool":{"should":[{"match":{"last_name":{"query":"Иванов","boost":6}}},{"match":{"last_name":{"query":"Иванов","operator":"and","boost":7}}},{"match":{"last_name":{"query":"Иванов","analyzer":"standard","boost":9}}},{"match":{"last_name":{"query":"Иванов","analyzer":"standard","operator":"and","boost":10}}},{"match":{"last_name":{"query":"Иванов","analyzer":"standard","fuzziness":2}}}]}}],"minimum_should_match":1}},"indices_boost":[{"memorial":1},{"podvig":2},{"pamyat":3}],"size":"10","from":0}


url0 = 'https://pamyat-naroda.ru/heroes/?last_name=%D0%B8%D0%B2%D0%B0%D0%BD%D0%BE%D0%B2&first_name=&middle_name=&date_birth=&adv_search=y'
headers['Host'] = 'pamyat-naroda.ru'
headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0'
headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
headers['Accept-Language'] = 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3'
headers['Accept-Encoding'] = 'gzip, deflate, br'
headers['Connection'] = 'keep-alive'
headers['Referer'] = 'https://pamyat-naroda.ru/'
headers['Cookie'] = 'BITRIX_PN_DATALINE_LNG=ru; PNSESSIONID=g6jA4ujCo5sCwzAGVgMKuyvS5WCHbMOl; bda88568a54f922fcdfc6dbf940e5d00='+cookie_00+'; r='+s.cookies['r']+'; 56105c9ab348522591eea18fbe4d080b='+s.cookies['r']
#headers['Cookie'] = 'BITRIX_PN_DATALINE_LNG=ru; PNSESSIONID=g6jA4ujCo5sCwzAGVgMKuyvS5WCHbMOl; bda88568a54f922fcdfc6dbf940e5d00='+cookie_00+'; r='+s.cookies['r']
headers['Upgrade-Insecure-Requests'] = '1'
headers['TE'] = 'Trailers'
res = requests.post(url0,headers=headers)
print(res.cookies)


headers={}
headers['Host'] = 'cdn.pamyat-naroda.ru'
headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0'
headers['Accept'] = '*/*'
headers['Accept-Language'] = 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3'
headers['Accept-Encoding'] = 'gzip, deflate, br'
headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
headers['Content-Length'] = '558'
headers['Origin'] = 'https://pamyat-naroda.ru'
headers['Connection'] = 'keep-alive'
headers['Referer'] = 'https://pamyat-naroda.ru/heroes/?last_name=%D0%B8%D0%B2%D0%B0%D0%BD%D0%BE%D0%B2&first_name=&middle_name=&date_birth=&adv_search=y'




url1 = 'https://cdn.pamyat-naroda.ru/data/'+a_bs[0]+'/'+b_bs[0]+'/memorial,podvig,pamyat/chelovek_vpp,chelovek_donesenie,vspomogatelnoe_donesenie,chelovek_gospital,chelovek_dopolnitelnoe_donesenie,chelovek_zahoronenie,chelovek_eksgumatsiya,chelovek_plen,chelovek_prikaz,chelovek_kartoteka_memorial,chelovek_nagrazhdenie,chelovek_predstavlenie,chelovek_kartoteka,chelovek_yubileinaya_kartoteka,commander,/_search'
#url1 = 'https://cdn.pamyat-naroda.ru/data/j4MkwWyuA7wh94YDC_dyww/1577188211/memorial,podvig,pamyat/chelovek_vpp,chelovek_donesenie,vspomogatelnoe_donesenie,chelovek_gospital,chelovek_dopolnitelnoe_donesenie,chelovek_zahoronenie,chelovek_eksgumatsiya,chelovek_plen,chelovek_prikaz,chelovek_kartoteka_memorial,chelovek_nagrazhdenie,chelovek_predstavlenie,chelovek_kartoteka,chelovek_yubileinaya_kartoteka,commander,/_search'

print(url1)
res = requests.post(url1,data=data)
print(res.text)