from requests_html import HTMLSession
import json,pprint

session = HTMLSession()
search_str = 'одесская обл'
maxNumRecords = '200'
firstRecordPosition = str(0)
xmlParam = f'<request firstRecordPosition="{firstRecordPosition}" maxNumRecords="{maxNumRecords}" countResults="true"><record f23="P~{search_str}" entity="Человек Награждение"></record><record f23="P~{search_str}" entity="Человек Представление"></record><record f23="P~{search_str}" entity="Человек Картотека"></record><record f23="P~{search_str}" entity="Человек Юбилейная Картотека"></record></request>'
payload = {'json': '1'}
payload['xmlParam']=xmlParam
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

#http://podvignaroda.ru/?#id=1006890324&tab=navDetailManCard

f_struct = {}
f_struct['id']='id'
f_struct['f2']='Фамилия'
f_struct['f3']='Имя'
f_struct['f4']='Отчество'
f_struct['f5']='Год рождения'
f_struct['f6']='Звание'
f_struct['f7']='В РККА с'
f_struct['f8']='Место призыва'
f_struct['f23']='Место рождения'


r = session.post("http://podvignaroda.ru/Image3/newsearchservlet", data=payload, headers=headers)


#for record in json.loads(r.text)['records']:
#    pprint.pprint(record)
result = json.loads(r.text)
if(result['result']=='OK'):
    count_pages = int(result['totalRecords'])//int(maxNumRecords)
    futures = [i for i in range(0, countPages)]
    for y in 

else:
    print('not OK')
#print(json.loads(r.text)['records'])
#print(r.text)