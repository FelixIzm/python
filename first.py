import requests, json
import bs4
import http.cookies


response=requests.get('https://obd-memorial.ru/html/search.htm?f=%D0%B8%D0%B2%D0%B0%D0%BD%D0%BE%D0%B2&n=&s=&y=&r=&p=4')

print (response.status_code) # Код ответа  
print (response.headers) # Заголовки ответа
print("========================")
#print (response.content) # Тело ответа
#print(response.cookies["3fbe47cd30daea60fc16041479413da2"])
#print(response.cookies["JSESSIONID"])
if(response.status_code==307):
    cookies = {'3fbe47cd30daea60fc16041479413da2': response.cookies["3fbe47cd30daea60fc16041479413da2"],'JSESSIONID': response.cookies["JSESSIONID"]}
    response=requests.get('https://obd-memorial.ru/html/search.htm?f=%D0%B8%D0%B2%D0%B0%D0%BD%D0%BE%D0%B2&n=&s=&y=&r=&p=2', cookies=cookies)
    print (response.status_code) # Код ответа  
    #print (response.headers) # Заголовки ответа
    #print (response.content) # Тело ответа
    #print(response.cookies.get_dict())
    #json_string = response.headers['Set-Cookie']
    #obj = json.loads(json_string)
    #print (response.headers) # Заголовки ответа
    cookies = http.cookies.SimpleCookie()
    cookies.load(response.headers['Set-Cookie'])
    #print(cookies.keys())
    #print(cookies.values())
    #print(cookies.items())

    print(cookies['search_ids'].value)
    '''
    for k, v in cookies.items():
        print(v.value)
    '''
else:
    print("ok")

# Запрос
#print (response.request.headers) # Заголовки отправленные с запросом
