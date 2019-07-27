from pymongo import MongoClient
import pymongo, json, xlrd, sys, pprint
from datetime import datetime

client = MongoClient('35.193.230.58',
    username='felix', password='12345678', 
    authSource='test',authMechanism='SCRAM-SHA-1')

db = client['test']
collection_name = 'short_field'

if collection_name not in db.list_collection_names():
    db.create_collection(collection_name)
#print(client.database_names())  

records = db[collection_name]

count_doc_start = records.count_documents({})

loc = ("C:\\BackUp\\Docs\\Южное Кладбище\\Выгрузки\\ниж_1.xlsx") 
#loc = ("E:\Южное Кладбище\VGD\csv\Калязинский_рн.xlsx")
loc = ("C:\\BackUp\\Docs\\Южное Кладбище\\Выгрузки\\москворецкий_рвк.xlsx") 
loc = ("C:\\BackUp\\Docs\\Южное Кладбище\\Выгрузки\\Киевская_обл.xlsx") 
loc = ("E:\Temp\obd\Киевская_обл.xlsx") 

fx_rec = '''{{
    "f0": {0},
    "f1": {1},
    "f2":"{2}",
    "f3":"{3}",
    "f4":"{4}",
    "f5":"{5}",
    "f6":"{6}",
    "f7":"{7}",
    "f8":"{8}",
    "f9":"{9}",
    "f10":"{10}",
    "f11":"{11}"
}}'''


start_time = datetime.now()
wb = xlrd.open_workbook(loc) 
sheet = wb.sheet_by_index(0) 

#sys.exit(0)

obj = sheet.get_rows()
obj.__next__()

'''
try:
    a_rec = [json.loads(fx_rec.format('"обд"', int(row[0].value), row[1].value, row[2].value, row[3].value, row[4].value, row[5].value, row[6].value, row[7].value,row[8].value, row[9].value, row[10].value)) for i, row in enumerate(obj) ]
except Exception as ex: 
    template = "Тип ошибки {0} \nArguments:{1!r}"
    message = template.format(type(ex).__name__, ex.args)
    print(message)
'''


a_rec=[]
for i, row in enumerate(obj):
    #print(int(row[0].value))
    try:
        a_rec.append(json.loads(fx_rec.format('"обд"', int(row[0].value), row[1].value, row[2].value, row[3].value, row[4].value, row[5].value, row[6].value, row[7].value,row[8].value, row[9].value, row[10].value)))
    except Exception as ex: 
        template = "Тип ошибки {0} \nArguments:{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        print(row)


try:
    records.insert_many(a_rec, ordered=False)
except pymongo.errors.BulkWriteError as e:
    print(e.details['writeErrors'])

count_doc_end = records.count_documents({})
#print(len(a_rec))
end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))
print('count docs = {0} end docs = {1} delta = {2}'.format(count_doc_start,count_doc_end,count_doc_end-count_doc_start))
