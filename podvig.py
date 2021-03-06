from requests_html import HTMLSession
import json,pprint,asyncio, sys, sqlite3, argparse

session = HTMLSession()
loop = asyncio.get_event_loop()

#######################
search_str = 'херсонская обл'
maxNumRecords = '200'
search_subject = 'f8' # f8 - призыв, f23 - место рождения
#######################
firstRecordPosition = str(0)
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

#conn = sqlite3.connect('./db/all_fields.db') # или :memory: чтобы сохранить в RAM
conn = sqlite3.connect('E:\\Temp\\db\\all_fields.db') # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()



def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument ('name', nargs='?')
    return parser
 
 
if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args()
    print(namespace)
    # если что-то передали в аргументах, удаляем таблицы и все заново
    if namespace.name:
        cursor.execute("DROP TABLE if exists search_ids")
        cursor.execute("DROP TABLE if exists pages")



# Создание таблицы

cursor.execute("CREATE TABLE if not exists pages (num integer)")
cursor.execute("CREATE TABLE if not exists search_ids (id integer, flag integer, csv text)")
cursor.execute("SELECT num FROM pages")
data = cursor.fetchone()
if data is None:
    cursor.execute('insert into pages(num) values (0)')
    conn.commit()
    insertedPages=int(0)
else:
    insertedPages = data[0]

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
    global maxNumRecords, search_str, search_subject
    xmlParam = f'<request firstRecordPosition="{firstRecordPosition}" maxNumRecords="{maxNumRecords}" countResults="true"><record {search_subject}="P~{search_str}" entity="Человек Награждение"></record><record {search_subject}="P~{search_str}" entity="Человек Представление"></record><record {search_subject}="P~{search_str}" entity="Человек Картотека"></record><record {search_subject}="P~{search_str}" entity="Человек Юбилейная Картотека"></record></request>'
    payload = {'json': '1'}
    payload['xmlParam']=xmlParam
    #print(xmlParam)
    r = session.post("http://podvignaroda.ru/Image3/newsearchservlet", data=payload, headers=headers)
    result = json.loads(r.text)
    if(result['result']=='OK'):
        #print(len(json.loads(r.text)['records']))
        return json.loads(r.text)['records']
    else:
        return 'not ok'

async def fxMain():
    global headers,countPages, totalRecords, search_str,maxNumRecords,insertedPages, search_subject
    maxNumRecordsLocal = '10'
    firstRecordPosition = str(0)
    xmlParam = f'<request firstRecordPosition="{firstRecordPosition}" maxNumRecords="{maxNumRecordsLocal}" countResults="true"><record {search_subject}="P~{search_str}" entity="Человек Награждение"></record><record {search_subject}="P~{search_str}" entity="Человек Представление"></record><record {search_subject}="P~{search_str}" entity="Человек Картотека"></record><record {search_subject}="P~{search_str}" entity="Человек Юбилейная Картотека"></record></request>'
    payload = {'json': '1'}
    payload['xmlParam']=xmlParam
    r = session.post("http://podvignaroda.ru/Image3/newsearchservlet", data=payload, headers=headers)
    result = json.loads(r.text)
    if(result['result']=='OK'):
        totalRecords = int(result['totalRecords'])
        countPages = int(result['totalRecords'])//int(maxNumRecords)
        print('\ntotalRecords  = {} \ncountPages    = {}\nmaxNumRecords = {}'.format(totalRecords,countPages,maxNumRecords))
        futures = [get_page(i) for i in range(insertedPages, int(result['totalRecords']), int(maxNumRecords))]
        for i, future in enumerate(futures):
            result = await future
            if(result!='not ok'):
                for rec in result:
                    db_json={}
                    for key, value in f_struct.items():
                        
                        try:
                            db_json[f_struct[key]] = rec[key]
                        except KeyError:
                            db_json[f_struct[key]]="''"
                    cursor.execute('insert into search_ids(id,flag,csv) values ('+rec['id']+',1,"'+str(db_json).replace('"',"")+'")')
                    conn.commit()

                print ('{} из {}'.format(str(insertedPages+i+1),str(countPages)))
                cursor.execute('update pages set num='+str(i+insertedPages+1))
                conn.commit()
    else:
        print('Result Not OK')

loop.run_until_complete(fxMain())
loop.close()