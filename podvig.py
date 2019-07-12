from requests_html import HTMLSession
import json,pprint,asyncio

session = HTMLSession()
loop = asyncio.get_event_loop()

search_str = 'херсонская обл'
maxNumRecords = '100'
firstRecordPosition = str(0)
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

countPages = 0
totalRecords = 0

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



async def get_page(firstRecordPosition):
    global maxNumRecords, search_str
    xmlParam = f'<request firstRecordPosition="{firstRecordPosition}" maxNumRecords="{maxNumRecords}" countResults="true"><record f23="P~{search_str}" entity="Человек Награждение"></record><record f23="P~{search_str}" entity="Человек Представление"></record><record f23="P~{search_str}" entity="Человек Картотека"></record><record f23="P~{search_str}" entity="Человек Юбилейная Картотека"></record></request>'
    payload = {'json': '1'}
    payload['xmlParam']=xmlParam
    #print(xmlParam)
    r = session.post("http://podvignaroda.ru/Image3/newsearchservlet", data=payload, headers=headers)
    result = json.loads(r.text)
    if(result['result']=='OK'):
        #print(len(json.loads(r.text)['records']))
        return len(json.loads(r.text)['records'])
    else:
        return 'not ok'

#for record in json.loads(r.text)['records']:
#    pprint.pprint(record)

# result = json.loads(r.text)
# if(result['result']=='OK'):
#     countPages = int(result['totalRecords'])//int(maxNumRecords)
#     futures = [i for i in range(0, int(result['totalRecords']), int(maxNumRecords))]
#     for y in enumerate(futures):
#         print(y)

# else:
#     print('not OK')

#print(json.loads(r.text)['records'])
#print(r.text)

async def fxMain():
    global headers,countPages, totalRecords, search_str,maxNumRecords
    maxNumRecordsLocal = '10'
    firstRecordPosition = str(0)
    xmlParam = f'<request firstRecordPosition="{firstRecordPosition}" maxNumRecords="{maxNumRecordsLocal}" countResults="true"><record f23="P~{search_str}" entity="Человек Награждение"></record><record f23="P~{search_str}" entity="Человек Представление"></record><record f23="P~{search_str}" entity="Человек Картотека"></record><record f23="P~{search_str}" entity="Человек Юбилейная Картотека"></record></request>'
    payload = {'json': '1'}
    payload['xmlParam']=xmlParam
    r = session.post("http://podvignaroda.ru/Image3/newsearchservlet", data=payload, headers=headers)
    result = json.loads(r.text)
    if(result['result']=='OK'):
        totalRecords = int(result['totalRecords'])
        countPages = int(result['totalRecords'])//int(maxNumRecords)
        print('\ntotalRecords  = {} \ncountPages    = {}\nmaxNumRecords = {}'.format(totalRecords,countPages,maxNumRecords))
        futures = [get_page(i) for i in range(0, int(result['totalRecords']), int(maxNumRecords))]
        #for y,page in enumerate(futures):
        #    print(y)
        for i, future in enumerate(futures):
            result = await future
            print("{} {}".format(i,result))


    else:
        print('Not OK')

loop.run_until_complete(fxMain())
loop.close()